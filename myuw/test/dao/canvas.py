from django.test import TestCase
from myuw.dao.canvas import _get_canvas_enrollment_dict_for_regid,\
    canvas_course_is_available, get_canvas_course_from_section,\
    get_canvas_course_url
from myuw.dao.schedule import _get_schedule
from restclients.sws.section import get_section_by_label
from myuw.dao.term import get_current_quarter
from myuw.test import fdao_sws_override, get_request_with_user, get_request


@fdao_sws_override
class TestCanvas(TestCase):
    def setUp(self):
        get_request()

    def test_crosslinks(self):
        data = _get_canvas_enrollment_dict_for_regid(
            "12345678901234567890123456789012")

        physics = data['2013,spring,PHYS,121/A']
        self.assertEquals(physics.course_url,
                          'https://canvas.uw.edu/courses/249652')

        self.assertTrue(canvas_course_is_available(physics.course_id))

        has_section_b = '2013,spring,TRAIN,100/B' in data
        self.assertTrue(has_section_b)

        has_section_a = '2013,spring,TRAIN,100/A' in data
        self.assertTrue(has_section_a)

        train = data['2013,spring,TRAIN,100/A']
        self.assertEquals(train.course_url,
                          'https://canvas.uw.edu/courses/249650')

    def test_get_canvas_course_url(self):
        sws_section = get_section_by_label('2013,spring,TRAIN,101/A')
        self.assertIsNotNone(get_canvas_course_from_section(sws_section))
        self.assertEquals(get_canvas_course_url(sws_section),
                          'https://canvas.uw.edu/courses/149651')
