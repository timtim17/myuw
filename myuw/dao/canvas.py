import logging
from re import search
from uw_canvas.enrollments import Enrollments
from uw_canvas.sections import Sections
from uw_canvas.courses import Courses
from uw_canvas.models import CanvasCourse, CanvasSection
from restclients_core.exceptions import DataFailureException
from myuw.dao import is_using_file_dao
from myuw.dao.pws import get_regid_of_current_user

logger = logging.getLogger(__name__)


def canvas_prefetch():
    def _method(request):
        return get_canvas_active_enrollments(request)
    return [_method]


def get_canvas_active_enrollments(request):
    if not hasattr(request, "canvas_act_enrollments"):
        request.canvas_act_enrollments = (
            Enrollments().get_enrollments_for_regid(
                get_regid_of_current_user(request),
                {'type': ['StudentEnrollment'], 'state': ['active']}))
    return request.canvas_act_enrollments


def set_section_canvas_course_urls(canvas_active_enrollments, schedule):
    """
    Set canvas_course_url in schedule.sections
    """
    section_labels = set()
    for section in schedule.sections:
        section_labels.add(section.section_label())

    canvas_links = {}
    for enrollment in canvas_active_enrollments:
        (sws_label, inst_regid) = sws_section_label(enrollment.sis_section_id)
        if sws_label is not None and sws_label in section_labels:
            canvas_links[sws_label] = enrollment.course_url

    sws_labels = sorted(canvas_links.keys())
    for section in schedule.sections:
        section_label = section.section_label()
        if (not section.is_ind_study() and
                len(section.linked_section_urls)):
            section_label = _get_secondary_section_label(
                section_label, sws_labels)
        section.canvas_course_url = canvas_links.get(section_label)


def _get_secondary_section_label(primary_section_label, sws_labels):
    for label in sws_labels:
        if search(primary_section_label, label):
            return label


def get_canvas_course_from_section(sws_section):
    try:
        return Courses().get_course_by_sis_id(
            sws_section.canvas_course_sis_id())
    except DataFailureException as err:
        if err.status == 404:
            return None
        raise ValueError


def get_canvas_course_url(sws_section, person):
    if sws_section.is_independent_study:
        sws_section.independent_study_instructor_regid = person.uwregid
    try:
        canvas_course = get_canvas_course_from_section(sws_section)
    except ValueError:
        return "error"
    if canvas_course:
        return canvas_course.course_url


def sws_section_label(sis_id):
    canvas_section = CanvasSection(sis_section_id=sis_id)
    sws_label = canvas_section.sws_section_id()
    if sws_label is None:
        canvas_course = CanvasCourse(sis_course_id=sis_id)
        sws_label = canvas_course.sws_course_id()
        return (sws_label, canvas_course.sws_instructor_regid())
    else:
        return (sws_label, canvas_section.sws_instructor_regid())


def get_viewable_course_sections(canvas_course_id, canvas_user_id):
    """
    Returns a list of academic sections in the course identified by
    canvas_course_id, for which the user identified by canvas_user_id can
    view enrollments.
    """
    limit_privileges_to_course_section = False
    limit_sections = {}

    enrollments = Enrollments().get_enrollments_for_course(
        canvas_course_id, params={'user_id': canvas_user_id})

    for enrollment in enrollments:
        if enrollment.limit_privileges_to_course_section:
            limit_privileges_to_course_section = True
            limit_sections[enrollment.section_id] = True

    viewable_sections = []
    for section in Sections().get_sections_in_course(canvas_course_id):
        if not section.is_academic_sis_id():
            continue

        if (limit_privileges_to_course_section and
                section.section_id not in limit_sections):
            continue

        viewable_sections.append(section)

    return viewable_sections
