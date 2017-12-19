from django.shortcuts import render
from django.template import RequestContext
from django.http import Http404
from datetime import datetime
import logging
from django.contrib.auth.decorators import login_required
from myuw.views.decorators import admin_required
from myuw.views import set_admin_wrapper_template
from myuw.dao import get_user_model
from myuw.dao.card_display_dates import get_values_by_date
from myuw.dao.card_display_dates import get_card_visibilty_date_values
from myuw.dao import is_using_file_dao
from myuw.dao.term import get_default_date, get_comparison_datetime, \
    get_default_datetime
from myuw.models import SeenRegistration
from django.test.client import RequestFactory
from uw_sws.term import get_term_by_date
from dateutil import tz
import pytz

DATE_KEYS = ['myuw_after_submission', 'myuw_after_last_day', 'myuw_after_reg',
             'myuw_before_finals_end', 'myuw_before_last_day',
             'myuw_before_end_of_reg_display', 'myuw_before_first_day',
             'myuw_before_end_of_first_week', 'myuw_after_eval_start',
             'in_coursevel_fetch_window']


@login_required
@admin_required('USERSERVICE_ADMIN_GROUP')
def override(request):
    logger = logging.getLogger(__name__)

    context = {}
    if request.method == "POST":
        _handle_post(request, context)

    set_admin_wrapper_template(context)

    add_session_context(request, context)
    add_date_term_info(request, context)

    add_seen_registration_context(request, context)
    return render(request, "display_dates/override.html", context)


def _handle_post(request, context):
    if request.POST["date"]:
        try:
            date_obj = datetime.strptime(request.POST["date"],
                                         "%Y-%m-%d %H:%M:%S")
            request.session["myuw_override_date"] = request.POST["date"]
        except Exception as ex:
            try:
                date_obj = datetime.strptime(request.POST["date"],
                                             "%Y-%m-%d")
                request.session["myuw_override_date"] = request.POST["date"]

            except Exception as ex:
                context["date_error"] = str(ex)

    else:
        if "myuw_override_date" in request.session:
            del request.session["myuw_override_date"]

    for val in DATE_KEYS:
        if val in request.POST:
            if request.POST[val] == "yes":
                request.session[val] = True
            elif request.POST[val] == "no":
                request.session[val] = False
            else:
                if val in request.session:
                    del request.session[val]
        else:
            if val in request.session:
                del request.session[val]


def add_date_term_info(request, context):
    actual_now = get_default_datetime()
    used_now = get_comparison_datetime(request)

    context["actual_now_date"] = str(actual_now)
    context["effective_now_date"] = str(used_now)
    context["is_using_mock_data"] = is_using_file_dao()

    try:
        actual_term = get_term_by_date(actual_now.date())
        context["actual_now_term_year"] = actual_term.year
        context["actual_now_term_quarter"] = actual_term.quarter
    except Exception as ex:
        pass

    try:
        used_term = get_term_by_date(used_now.date())
        context["effective_now_term_year"] = used_term.year
        context["effective_now_term_quarter"] = used_term.quarter
    except Exception as ex:
        pass


def add_session_context(request, context):
    if "myuw_override_date" in request.session:
        context["myuw_override_date"] = request.session["myuw_override_date"]

    for val in DATE_KEYS:
        if val in request.session:
            if request.session[val] is True:
                context["%s_true" % val] = True
            else:
                context["%s_false" % val] = True
        else:
            context["%s_unset" % val] = True

    now_request = RequestFactory().get("/")
    now_request.session = {}
    context["values_used"] = get_card_visibilty_date_values(request)

    now = datetime.now()
    default = get_default_date()

    used_date = datetime(default.year, default.month, default.day, now.hour,
                         now.minute, now.second)
    context["values_now"] = get_values_by_date(used_date, now_request)


def add_seen_registration_context(request, context):
    user = get_user_model()

    seen_registrations = SeenRegistration.objects.filter(user=user)
    seen = []

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    to_zone = pytz.timezone("America/Los_Angeles")

    for reg in seen_registrations:

        seen_date = reg.first_seen_date
        utc = seen_date.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)

        seen.append({
            'year': reg.year,
            'quarter': reg.quarter,
            'summer': reg.summer_term,
            'date_seen': local.__str__(),
        })

    context['seen_registrations'] = seen
