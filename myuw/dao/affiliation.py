"""
This module provides affiliations of the current user
"""

import logging
from myuw.dao.enrollment import get_main_campus
from myuw.dao.gws import is_grad_student, is_student, is_undergrad_student,\
    is_pce_student, is_student_employee, is_staff_employee,\
    is_seattle_student, is_bothell_student, is_tacoma_student,\
    is_applicant, is_grad_c2, is_undergrad_c2, no_affiliation
from myuw.dao.instructor_schedule import is_instructor
from myuw.dao.pws import get_employee_campus, is_employee
from myuw.dao.term import get_current_quarter
from myuw.dao.thrive import is_fyp, is_aut_transfer, is_win_transfer
from myuw.dao.uwnetid import is_clinician, is_2fa_permitted, is_faculty
from myuw.dao.exceptions import IndeterminateCampusException


logger = logging.getLogger(__name__)


def get_all_affiliations(request):
    """
    return a dictionary of affiliation indicators.
    ["student"]: True if the user is currently an UW student.
    ["grad"]: True if the user is currently an UW graduate student.
    ["undergrad"]: True if the user is currently an UW undergraduate student.
    ["applicant"]: True if the user is currently a UW applicant
    ["pce"]: True if the user is currently an UW PCE student.
    ["grad_c2"]: True if the user is an UW PCE grad student.
    ["undergrad_c2"]: True if the user is an UW PCE undergrad student.
    ["employee"]: True if the user is currently a uw employee.
    ["stud_employee"]: True if the user is currently a student employee.
    ["faculty"]: True if the user is currently faculty.
    ["seattle"]: True if the user is an UW Seattle student
                 in the current quarter.
    ["bothell"]: True if the user is an UW Bothell student
                 in the current quarter.
    ["tacoma"]: True if the user is an UW Tacoma student
                in the current quarter.
    ["official_seattle"]: True if the user is an UW Seattle student
                 according to the SWS Enrollment.
    ["official_bothell"]: True if the user is an UW Bothell student
                 according to the SWS Enrollment.
    ["official_tacoma"]: True if the user is an UW Tacoma student
                according to the SWS Enrollment.
    ["official_pce"]: True if the user is an UW PCE student
                according to the SWS Enrollment.
    """
    if hasattr(request, 'myuw_user_affiliations'):
        return request.myuw_user_affiliations

    is_fy_stud = is_fyp(request)
    is_aut_xfer = is_aut_transfer(request)
    is_win_xfer = is_win_transfer(request)
    is_hxt_viewer = get_is_hxt_viewer(request,
                                      is_fy_stud, is_aut_xfer,
                                      is_win_xfer)
    data = {"grad": is_grad_student(request),
            "undergrad": is_undergrad_student(request),
            "applicant": is_applicant(request),
            "student": is_student(request),
            "pce": is_pce_student(request),
            "grad_c2": is_grad_c2(request),
            "undergrad_c2": is_undergrad_c2(request),
            "staff_employee": is_staff_employee(request),
            "stud_employee": is_student_employee(request),
            "employee": is_employee(request),
            "fyp": is_fy_stud,
            "aut_transfer": is_aut_xfer,
            "win_transfer": is_win_xfer,
            "faculty": is_faculty(request),
            "clinician": is_clinician(request),
            "2fa_permitted": is_2fa_permitted(request),
            "instructor": is_instructor(request),
            "seattle": is_seattle_student(request),
            "bothell": is_bothell_student(request),
            "tacoma": is_tacoma_student(request),
            "hxt_viewer": is_hxt_viewer,
            "no_affi": no_affiliation(request),
            }

    campuses = []
    if data["student"]:
        # determine student campus based on current and future enrollments
        try:
            campuses = get_main_campus(request)
        except IndeterminateCampusException:
            pass

    if data["employee"]:
        # determine employee primary campus based on their mailstop
        try:
            campuses = [get_employee_campus(request)]
        except IndeterminateCampusException:
            pass

    official_campuses = _get_official_campuses(campuses)
    data = dict(data.items() + official_campuses.items())
    request.myuw_user_affiliations = data
    return data


def _get_official_campuses(campuses):
    official_campuses = {'official_seattle': False,
                         'official_bothell': False,
                         'official_tacoma': False}
    if 'Bothell' in campuses:
        official_campuses['official_tacoma'] = True
    if 'Seattle' in campuses:
        official_campuses['official_seattle'] = True
    if 'Tacoma' in campuses:
        official_campuses['official_bothell'] = True
    return official_campuses


def get_base_campus(affiliations):
    """
    Return one currently enrolled campus.
    If not exist, return one affiliated campus.
    """
    campus = ""
    try:
        if affiliations["official_seattle"]:
            campus = "seattle"
        if affiliations["official_bothell"]:
            campus = "bothell"
        if affiliations["official_tacoma"]:
            campus = "tacoma"
        if affiliations["undergrad_c2"] or affiliations["grad_c2"]:
            campus = "pce"
    except KeyError:
        try:
            if affiliations["seattle"]:
                campus = "seattle"
            if affiliations["bothell"]:
                campus = "bothell"
            if affiliations["tacoma"]:
                campus = "tacoma"
        except KeyError:
            campus = ""
            pass
    return campus


def get_is_hxt_viewer(request,
                      is_fyp, is_aut_transfer, is_win_transfer):
    is_viewer = False
    if is_seattle_student(request) and\
       is_undergrad_student(request) and\
       not is_fyp:
        term = get_current_quarter(request)
        if term.quarter == 'winter':
            is_viewer = not is_win_transfer
        elif term.quarter == 'autumn':
            is_viewer = not is_aut_transfer
        else:
            is_viewer = True
    return is_viewer


def get_identity_log_str(affi):
    """
    Return "(Affiliations: <affiliations>, <campus codes>)"
    """
    res = "(Affiliations:"
    no_affiliation_lengthmark = len(res)
    if affi["grad"]:
        res += ' Grad'
    if affi["undergrad"]:
        res += ' Undergrad'
    if affi["pce"]:
        res += ' PCE-student'
    if affi["grad_c2"]:
        res += ' Grad_C2'
    if affi["undergrad_c2"]:
        res += ' Undergrad_C2'
    if affi["faculty"]:
        res += ' Faculty'
    if affi["staff_employee"]:
        res += ' Staff'
    if affi["instructor"]:
        res += ' Instructor'
    if affi["clinician"]:
        res += 'Clinician'
    if affi["employee"]:
        res += ' Employee'
    if len(res) == no_affiliation_lengthmark:
        res += 'None'

    res += ', Campuses:'
    no_campus_lengthmark = len(res)
    if affi["seattle"] or affi["official_seattle"]:
        res += ' Seattle'
    if affi["bothell"] or affi["official_bothell"]:
        res += ' Bothell'
    if affi["tacoma"] or affi["official_tacoma"]:
        res += ' Tacoma'
    if len(res) == no_campus_lengthmark:
        res += 'None'
    res += ') '
    return res
