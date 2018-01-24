import logging
from myuw.models import UserMigrationPreference
from myuw.dao import _is_optin_user as is_optin_user
from myuw.dao import get_netid_of_current_user
from myuw.dao.gws import (is_staff_employee, is_student_employee,
                          is_undergrad_student, is_current_graduate_student,
                          is_employee,  is_faculty, is_applicant)

logger = logging.getLogger(__name__)


def set_preference_to_new_myuw(uwnetid):
    obj, is_new = UserMigrationPreference.objects.get_or_create(
        username=uwnetid)
    obj.use_legacy_site = False
    obj.save()


def set_preference_to_old_myuw(uwnetid):
    obj, is_new = UserMigrationPreference.objects.get_or_create(
        username=uwnetid)
    obj.use_legacy_site = True
    obj.save()


def has_legacy_preference(uwnetid):
    try:
        saved = UserMigrationPreference.objects.get(username=uwnetid)
        if saved.use_legacy_site:
            return True
    except UserMigrationPreference.DoesNotExist:
        pass
    return False


def has_newmyuw_preference(uwnetid):
    try:
        saved = UserMigrationPreference.objects.get(username=uwnetid)
        if saved and not saved.use_legacy_site:
            return True
    except UserMigrationPreference.DoesNotExist:
        pass
    return False


def is_oldmyuw_user(request):
    uwnetid = get_netid_of_current_user(request)
    if has_newmyuw_preference(uwnetid) or is_optin_user(uwnetid):
        return False
    if has_legacy_preference(uwnetid):
        return True
    if is_staff_employee(request):
        return True
    if is_faculty(request):
        return True
    if is_current_graduate_student(request):
        return True
    if is_undergrad_student(request):
        return False
    if is_applicant(request):
        return False
    return True
