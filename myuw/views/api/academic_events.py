# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import timedelta, date, datetime
import re
import json
import logging
import traceback
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.dao.instructor import is_instructor
from myuw.dao.term import get_comparison_date, get_current_quarter
from uw_trumba import get_calendar_by_name
from uw_sws.term import get_term_after

CURRENT_LIST_MAX_DAYS = 3
logger = logging.getLogger(__name__)


class AcademicEvents(ProtectedAPI):
    """
    Performs actions on /api/v1/academic_events
    """
    def get(self, request, *args, **kwargs):
        current = kwargs.get('current', False)
        timer = Timer()
        try:
            events = []

            cal_names = ['sea_acad-inst', 'sea_acad-holidays']
            if is_instructor(request):
                cal_names = cal_names + ['sea_acad-regi', 'sea_acad-grade']

            calendars = []
            for cal in cal_names:
                calendars.append(get_calendar_by_name(cal))

            raw_events = []
            index = 0
            for calendar in calendars:
                for event in calendar.walk('vevent'):
                    event.add("calendar_name", cal_names[index])
                    raw_events.append(event)
                index = index + 1

            raw_events = self.sort_events(raw_events)

            raw_events = self.categorize_events(raw_events)

            raw_events = self.filter_past_events(request, raw_events)

            if current:
                raw_events = self.filter_non_current(request, raw_events)
            else:
                raw_events = self.filter_too_future_events(request, raw_events)

            for event in raw_events:
                events.append(self.json_for_event(event, request))
            log_api_call(timer, request, "Get AcademicEvents")
            return self.json_response(events)
        except Exception:
            return handle_exception(logger, timer, traceback)

    def json_for_event(self, event, request):
        year, quarter = self.parse_year_quarter(event)
        # MUWM-4033 if event in current quarter use that year/qtr as backup
        if None in (year, quarter):
            year, quarter = self._get_year_qtr_from_cur_term(event, request)
        start, end = self.parse_dates(event)
        category = self.parse_category(event)
        categories = self.parse_myuw_categories(event)
        event_url = self.parse_event_url(event)

        is_all_day = self.parse_event_is_all_day(event)

        return {
            "summary": event.get('summary'),
            "start": start,
            "end": end,
            "year": year,
            "quarter": quarter,
            "category": category.to_ical(),
            "myuw_categories": categories,
            "event_url": event_url,
            "is_all_day": is_all_day,
        }

    def _get_year_qtr_from_cur_term(self, event, request):
        current = get_current_quarter(request)
        start = self.get_start_date(event)
        if current.first_day_quarter <= start <= current.last_final_exam_date:
            return current.year, current.quarter.capitalize()
        return None, None

    def parse_myuw_categories(self, event):
        return json.loads(event.get('myuw_categories'))

    def parse_event_is_all_day(self, event):
        start = event.get('dtstart')
        end = event.get('dtend')

        diff = end.dt - start.dt
        if diff.days == 1 and diff.seconds == 0:
            return True

        return False

    def parse_category(self, event):
        return event.get('categories')

    def parse_event_url(self, event):
        uid = event.get('uid')

        matches = re.match(r'.*?(\d+)$', uid)
        if not matches:
            return

        event_id = matches.group(1)

        url = ("http://www.washington.edu/calendar/academic/"
               "?trumbaEmbed=view%3Devent%26eventid%3D{}".format(event_id))

        return url

    def parse_dates(self, event):
        return (self.format_datetime(event.get('dtstart')),
                self.format_native_datetime(self.event_end_date(event)))

    def event_end_date(self, event):
        return self.get_end_date(event) - timedelta(days=1)

    def parse_year_quarter(self, event):
        desc = event.get('description')

        year = None
        quarter = None
        if not desc:
            return year, quarter

        matches = re.match(r".*Year: (\d{4})\s+Quarter: (\w+).*", desc)
        if matches:
            year = matches.group(1)
            quarter = matches.group(2)

        else:
            matches = re.match(r".*Year: (\d{4}).*", desc)
            if matches:
                year = matches.group(1)

        override = event.get('override_quarter')
        if override:
            quarter = override
        return year, quarter

    def format_datetime(self, dt):
        return self.format_native_datetime(dt.dt)

    def format_native_datetime(self, dt):
        return str(dt)

    def categorize_events(self, events):
        for event in events:
            categories = json.dumps(self.get_event_categories(event))
            event.add("myuw_categories", categories)

            # Breaks are clustered around winter and summer terms.
            # That's not convenient for us, so put them on the term we want!
            if 'term_breaks' in categories:
                summary = event.get('summary')
                matches = re.match(r'.*?([a-zA-Z]+) break.*', summary,
                                   flags=re.IGNORECASE)
                quarter = matches.group(1)
                event.add("override_quarter", quarter)

        return events

    def get_event_categories(self, event):
        categories = {'all': True}

        calendar_name = event.get("calendar_name")

        if "sea_acad-grade" == calendar_name:
            categories["grade"] = True

        if "sea_acad-regi" == calendar_name:
            categories["registration"] = True

        if "sea_acad-holidays" == calendar_name:
            categories["breaks"] = True

        if "sea_acad-inst" == calendar_name:
            categories["classes"] = True

            summary = event.get('summary')
            if summary and re.match(r'.*break.*', summary,
                                    flags=re.IGNORECASE):
                categories["breaks"] = True
                categories["term_breaks"] = True

        return categories

    def get_start_date(self, event):
        start = event.get('dtstart').dt
        if isinstance(start, datetime):
            start = start.date()
        return start

    def get_end_date(self, event):
        end = event.get('dtend').dt
        if isinstance(end, datetime):
            end = end.date()
        return end

    def sort_events(self, events):
        return sorted(events,
                      key=lambda e: self.get_start_date(e)
                      )

    def filter_past_events(self, request, events):
        comparison_date = get_comparison_date(request)

        non_past = []
        for event in events:
            # Events' end dates are midnight of the next day - not what we want
            # muwm-2489
            end_date = self.event_end_date(event)
            if end_date >= comparison_date:
                non_past.append(event)

        return non_past

    def filter_too_future_events(self, request, events):
        current = get_current_quarter(request)
        after = get_term_after

        last_date = None
        # MUWM-2522
        # This is intended as a workaround for missing data, but it's proably
        # also good enough if there's an error fetching a term resource
        # against live resources.
        try:
            last = after(after(after(after(current))))
            last_date = last.grade_submission_deadline.date()
        except Exception as ex:
            last_dt = (current.grade_submission_deadline + timedelta(days=365))
            last_date = last_dt.date()

        not_too_future = []
        for event in events:
            start = self.get_start_date(event)
            if start <= last_date:
                not_too_future.append(event)

        return not_too_future

    def filter_non_current(self, request, events):
        comparison_date = get_comparison_date(request)
        last_date = comparison_date + timedelta(days=7*4)

        ok_overlaps = {}
        round1 = []
        for event in events:
            if self.get_start_date(event) <= last_date:
                # The comparison date is the first date of the event in
                # the ideal event window (now -> 4 weeks from now)
                start = self.get_start_date(event)
                if start < comparison_date:
                    start = comparison_date

                date_string = self.format_native_datetime(start)
                # We only want to show events from the first 3 days that
                # overlap though
                if date_string not in ok_overlaps:
                    if len(ok_overlaps.keys()) >= CURRENT_LIST_MAX_DAYS:
                        # We've hit our 4th day -
                        # return the values we've collected
                        return round1
                    else:
                        # Track the new date
                        ok_overlaps[date_string] = True

                # This event is in that first 3 matching days
                round1.append(event)
            else:
                start = self.get_start_date(event)
                date_string = self.format_native_datetime(start)
                # There's an event outside of 4 weeks.  3 things can happen:
                # 1) we already have events, and the event's start date isn't
                #    in the ok_overlaps lookup
                #    - return what we have, we're outside the window
                # 2) we don't have any events
                #    - this is the first event, and it's outside the ideal
                #      window.  we want to show all events from this day
                # 3) we have events, and today's date is in ok_overlaps.
                #    - this is not the first event of the day, but it is a day
                #      of events we want to include.
                if len(round1) == 0:
                    # Case 2
                    ok_overlaps[date_string] = True
                if date_string in ok_overlaps:
                    # Case 3, or a continuation of case 2
                    round1.append(event)
                else:
                    # Case 1
                    return round1

        # If all of our events were in the first 3 days...
        return round1
