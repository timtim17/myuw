# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from restclients_core.exceptions import DataFailureException
from uw_myplan import get_plan
from myuw.dao.pws import get_regid_of_current_user
from uw_sws.section import get_section_by_label
from myuw.dao.card_display_dates import during_myplan_peak_load
from myuw.dao.term import get_current_quarter, get_comparison_datetime
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call, log_err
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class MyPlan(ProtectedAPI):
    """
    Performs actions on /api/v1/myplan
    """
    def get(self, request, *args, **kwargs):
        year = kwargs.get("year")
        quarter = kwargs.get("quarter")
        timer = Timer()
        try:
            no_myplan_access = during_myplan_peak_load(
                get_comparison_datetime(request), request)
            if no_myplan_access:
                log_msg(logger, timer,
                        "No MyPlan access during their peak load, abort!")
                return self.json_response([])

            plan = get_plan(regid=get_regid_of_current_user(request),
                            year=year,
                            quarter=quarter.lower(),
                            terms=1)
            base_json = plan.json_data()
            has_ready_courses = False
            has_unready_courses = False
            ready_count = 0
            unready_count = 0
            has_sections = False

            for course in base_json["terms"][0]["courses"]:
                if course["registrations_available"]:
                    has_ready_courses = True
                    ready_count = ready_count + 1
                    for section in course["sections"]:
                        has_sections = True
                        curriculum = course["curriculum_abbr"].upper()
                        section_id = section["section_id"].upper()
                        label = "{},{},{},{}/{}".format(
                            year,
                            quarter.lower(),
                            curriculum,
                            course["course_number"],
                            section_id)

                        sws_section = get_section_by_label(label)
                        section["section_data"] = sws_section.json_data()
                else:
                    if len(course["sections"]):
                        has_sections = True
                    has_unready_courses = True
                    unready_count = unready_count + 1

            base_json["terms"][0]["has_ready_courses"] = has_ready_courses
            base_json["terms"][0]["has_unready_courses"] = has_unready_courses
            base_json["terms"][0]["ready_count"] = ready_count
            base_json["terms"][0]["unready_count"] = unready_count
            base_json["terms"][0]["has_sections"] = has_sections

            log_api_call(timer, request, "Get MyPlan")
            return self.json_response(base_json)
        except Exception:
            log_err(logger, timer, traceback)
            return self.json_response([])
