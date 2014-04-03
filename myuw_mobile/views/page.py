from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings
import logging
from userservice.user import UserService
from myuw_mobile.dao.term import get_current_quarter
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_invalid_netid_response, log_success_response_with_affiliation
from myuw_mobile.views.rest_dispatch import invalid_session

#@mobile_template('{mobile/}index.html')
def index(request,
          year=None, 
          quarter=None,
          summer_term=None):
    timer = Timer()
    logger = logging.getLogger('myuw_mobile.views.page.index')

    context = {"year": year,
               "quarter": quarter,
               "summer_term": summer_term,
               "home_url": "/mobile",
               "err": None,
               "netid": None}

    netid = UserService().get_user()
    if not netid:
        log_invalid_netid_response(logger, timer)
        return invalid_session()

    context["netid"] = netid
    if year is None or quarter is None:
        cur_term = get_current_quarter()
        if cur_term is None:
            context["err"] = "No current quarter data!"
            log_data_not_found_response(logger, timer)
        else:
            context["year"] = cur_term.year
            context["quarter"] = cur_term.quarter
    else:
        pass
    log_success_response_with_affiliation(logger, timer)
    return render_to_response("index.html",
                              context,
                              context_instance=RequestContext(request))




