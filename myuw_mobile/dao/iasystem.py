from datetime import datetime
from django.utils import timezone
from restclients.pws import PWS
from restclients.exceptions import DataFailureException
from restclients.iasystem import evaluation
from myuw_mobile.dao.student_profile import get_profile_of_current_user
from myuw_mobile.dao.term import get_comparison_date, term_matched,\
    get_bof_7d_before_last_instruction, get_eof_term


def get_evaluations_by_section(section):
    return _get_evaluations_by_section_and_student(
        section, get_profile_of_current_user().student_number)


def _get_evaluations_by_section_and_student(section, student_id):
    try:
        search_params = {'year': section.term.year,
                         'term_name': section.term.quarter.capitalize(),
                         'curriculum_abbreviation': section.curriculum_abbr,
                         'course_number': section.course_number,
                         'section_id': section.section_id,
                         'student_id': student_id}
        return evaluation.search_evaluations(section.course_campus.lower(),
                                             **search_params)

    except DataFailureException:
        return None


def json_for_evaluation(request, evaluations, section_summer_term):
    if evaluations is None:
        return None
    local_tz = timezone.get_current_timezone()
    today = get_comparison_date(request)
    now = local_tz.localize(
        datetime(today.year, today.month, today.day, 0, 0, 1))

    # the start date of the default show window
    show_date = get_bof_7d_before_last_instruction(request)
    on_dt = local_tz.localize(
        datetime(show_date.year, show_date.month, show_date.day, 0, 0, 0))

    # the end date of the default show window
    hide_date = get_eof_term(request, True)

    term_off_dt = local_tz.localize(
        datetime(hide_date.year, hide_date.month, hide_date.day, 0, 0, 0))
    pws = PWS()
    json_data = []
    for evaluation in evaluations:
        off_dt = term_off_dt
        if term_matched(request, section_summer_term):
            json_item = {'instructors': [],
                         'url': None,
                         'is_multi_instr': False,
                         'close_date': None}

            if now < on_dt or now < evaluation.eval_open_date:
                continue

            if evaluation.eval_close_date < off_dt:
                off_dt = evaluation.eval_close_date

            if now >= off_dt:
                continue

            json_item['is_multi_instr'] = len(evaluation.instructor_ids) > 1
            for eid in evaluation.instructor_ids:
                instructor_json = {}
                instructor = pws.get_person_by_employee_id(eid)
                instructor_json['instructor_name'] = instructor.display_name
                instructor_json['instructor_title'] = instructor.title1
                json_item['instructors'].append(instructor_json)

            json_item['url'] = evaluation.eval_url
            json_item['close_date'] = off_dt.isoformat()
            json_data.append(json_item)

    return json_data

# def get_evaluations_for_student_term(term):
#     profile = get_profile_of_current_user()
#     return _get_evaluation_by_student_number(profile.student_number, term)
#
#
# def _get_evaluation_by_student_number(student_number, term):
#     seattle = None
#     bothell = None
#     tacoma = None
#     try:
#         seattle = evaluation.search_evaluations("seattle",
#                                                 year=term.year,
#                                                 term_name=term.quarter.capitalize(),
#                                                 student_id=student_number)
#     except DataFailureException:
#         pass
#     try:
#         tacoma = evaluation.search_evaluations("tacoma",
#                                                year=term.year,
#                                                term_name=term.quarter.capitalize(),
#                                                student_id=student_number)
#     except DataFailureException:
#         pass
#     try:
#         bothell = evaluation.search_evaluations("bothell",
#                                                 year=term.year,
#                                                 term_name=term.quarter.capitalize(),
#                                                 student_id=student_number)
#     except DataFailureException:
#         pass
#
#     return {'seattle': seattle,
#             'bothell': bothell,
#             'tacoma': tacoma}
