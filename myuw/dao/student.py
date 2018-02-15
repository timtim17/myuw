"""
This module will provide a method to retrieve all user majors, class standings
and minors along with current and rollup variables to facilitate
determinations about user context in the case that a user is not
enrolled for the current quarter
"""
from myuw.dao.enrollment import enrollment_search_by_regid
from uw_sws.term import get_current_term


def get_student_status(regid):
    """
    This will return a dictionary with the student status over time alongside
    various rollup variables
    :param regid:
    :return: dict
    """
    enrollments = enrollment_search_by_regid(regid)

    return {
        'majors': _get_majors(enrollments),
        'class_level': _get_class_standings(enrollments)
    }


def get_majors(regid):
    """
    Returns a dictionary with a dict of majors by terms in the 'majors'
    attribute, and a 'current' and 'rollup' major field
    :param regid
    :return: dict
    """
    enrollments = enrollment_search_by_regid(regid)

    return _get_majors(enrollments)


def get_rollup_and_future_majors(majors):
    return _get_rollup_and_future(majors['majors'], majors['rollup'])


def _get_majors(enrollments):
    return _process_fields(enrollments, "majors")


def get_minors(regid):
    """
    Returns a dictionary with a dict of majors by terms in the 'majors'
    attribute, and a 'current' and 'rollup' major field
    :param regid
    :return: dict
    """
    enrollments = enrollment_search_by_regid(regid)

    return _get_minors(enrollments)


def get_rollup_and_future_minors(minors):
    return _get_rollup_and_future(minors['minors'], minors['rollup'])


def _get_minors(enrollments):
    return _process_fields(enrollments, "minors")


def get_class_standings(regid):
    """
    Returns a dictionary with a dict of majors by terms in the majors
    attribute, and a 'current' and 'rollup' major field
    :param regid
    :return: dict
    """
    enrollments = enrollment_search_by_regid(regid)

    return _get_class_standings(enrollments)


def _get_class_standings(enrollments):
    return _process_fields(enrollments, "class_level")


def _process_fields(enrollments, attribute):
    obj = {}

    current_term = get_current_term()

    if current_term in enrollments:
        obj['current'] = getattr(enrollments[current_term], attribute)

    obj[attribute] = {term: getattr(enrollments[term], attribute)
                      for term in enrollments}

    if 'current' not in obj:
        sorted_terms = sorted(enrollments.keys())

        has_future_entry = False

        for term in sorted_terms:
            if term > current_term:
                obj['rollup'] = getattr(enrollments[term], attribute)
                has_future_entry = True
                break

        most_recent_term = sorted_terms[0]

        if not has_future_entry:
            for term in sorted_terms:
                if term > most_recent_term:
                    most_recent_term = term

            obj['rollup'] = getattr(enrollments[most_recent_term], attribute)
    else:
        obj['rollup'] = obj['current']

    return obj


def _get_rollup_and_future(obj, rollup):
    objects = []
    current_term = get_current_term()

    for term in obj.keys():
        list_value = obj[term]
        for item in list_value:
            if term > current_term and item not in objects:
                objects.append(item)

    for item in rollup:
        if item not in objects:
            objects.append(item)

    return objects
