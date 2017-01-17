import json
from myuw.test.api import (MyuwApiTest, require_url, fdao_pws_override,
                           fdao_sws_override, fdao_uwnetid_override)


@fdao_sws_override
@fdao_pws_override
@fdao_uwnetid_override
@require_url('myuw_profile_api')
class TestProfile(MyuwApiTest):

    def get_profile_response(self):
        return self.get_response_by_reverse('myuw_profile_api')

    def test_javerage(self):
        self.set_user('javerage')
        response = self.get_profile_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data["display_name"], "J. Average Student")
        self.assertEquals(data["first_name"], "John Joseph")
        self.assertEquals(data["last_name"], "Average")
        self.assertEquals(data["local_address"]["street_line1"],
                          "4634 26th Ave NE")
        self.assertEquals(data["local_address"]["zip_code"], "98105-4566")
        self.assertEquals(data["student_number"], "1033334")

        self.assertEquals(data["campus"], "Seattle")
        self.assertEquals(data["class_level"], "SENIOR")
        self.assertEquals(len(data["majors"]), 1)
        self.assertEquals(len(data["minors"]), 1)
        self.assertFalse(data["is_grad_student"])

        self.assertIsNotNone(data["password"])
        pw_data = data["password"]
        self.assertEquals(pw_data["last_change"], "2013-01-27 10:49:42-08:00")
        self.assertFalse(pw_data["has_active_med_pw"])
        self.assertIsNone(pw_data["last_change_med"])
        self.assertIsNone(pw_data["expires_med"])

    def test_bothell_campus(self):
        self.set_user("jbothell")
        response = self.get_profile_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data["campus"], "Bothell")

    def test_tacoma_campus(self):
        self.set_user("eight")
        response = self.get_profile_response()
        data = json.loads(response.content)
        self.assertEquals(data["campus"], "Tacoma")

    def test_staff(self):
        self.set_user("staff")
        self.set_date("2014-01-10")
        response = self.get_profile_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data["is_student"])
        self.assertFalse(data["is_grad_student"])
        self.assertIsNotNone(data["password"])
        pw_data = data["password"]
        self.assertTrue(pw_data["has_active_med_pw"])
        self.assertEquals(pw_data["last_change_med"],
                          "2013-02-03 10:57:06-07:00")
        self.assertEquals(pw_data["expires_med"],
                          "2013-06-03 10:57:06-08:00")
        self.assertTrue(pw_data["med_pw_expired"])

    def test_jerror(self):
        self.set_user("jerror")
        response = self.get_profile_response()
        self.assertEquals(response.status_code, 543)

        self.set_user("nouser")
        response = self.get_profile_response()
        self.assertEquals(response.status_code, 404)

        self.set_user('none')
        response = self.get_profile_response()
        self.assertEquals(response.status_code, 200)
