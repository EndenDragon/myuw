from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.sws.section import get_section_by_label
from restclients.models.sws import Term
from myuw.dao.mailman import get_single_email_list_by_section,\
    get_single_email_list, get_email_lists_by_term, get_section_email_lists,\
    get_all_secondary_section_lists
from myuw.test import fdao_sws_override, fdao_mailman_override, get_request,\
    get_request_with_user


@fdao_mailman_override
@fdao_sws_override
class TestMailmanDao(TestCase):
    def setUp(self):
        get_request()

    def test_get_single_email_list(self):
        list_data = get_single_email_list('B BIO', 180, 'A', 'summer', 2013)
        self.assertEqual(
            list_data["list_admin_url"],
            "https://mailman.u.washington.edu/mailman/admin/bbio180a_su13")
        self.assertEqual(
            list_data["list_address"], 'bbio180a_su13')
        self.assertTrue(list_data["list_exists"])

    def test_get_all_secondary_section_lists(self):
        primary_section = get_section_by_label('2013,spring,PHYS,121/A')
        sec_lists = get_all_secondary_section_lists(primary_section)
        self.assertEqual(len(sec_lists), 21)
        list1 = sec_lists[0]
        self.assertEqual(list1["list_address"], 'phys121aa_sp13')
        self.assertTrue(list1["list_exists"])
        list21 = sec_lists[20]
        self.assertEqual(list21["list_address"], 'phys121av_sp13')
        self.assertTrue(list21["list_exists"])

    def test_get_single_email_list_by_section(self):
        list_data = get_single_email_list_by_section(
            get_section_by_label('2013,summer,B BIO,180/A'))
        self.assertEqual(list_data["list_address"], 'bbio180a_su13')
        self.assertTrue(list_data["list_exists"])
        list_data = get_single_email_list_by_section(
            get_section_by_label('2013,summer,B BIO,180/AA'))
        self.assertEqual(list_data["list_address"], 'bbio180aa_su13')
        self.assertTrue(list_data["list_exists"])
        list_data = get_single_email_list_by_section(
            get_section_by_label('2013,spring,T ARTS,110/A'))
        self.assertEqual(list_data["list_address"], 'tarts110a_sp13')
        self.assertTrue(list_data["list_exists"])

    def test_get_section_email_lists(self):
        ret_json = get_section_email_lists(
            get_section_by_label('2013,spring,PHYS,121/A'))
        self.assertEqual(ret_json["course_abbr"], "PHYS")
        self.assertEqual(ret_json["course_number"], "121")
        self.assertEqual(ret_json["section_id"], "A")
        self.assertEqual(ret_json["is_primary"], True)
        self.assertEqual(ret_json["primary_list"]["list_address"],
                         'phys121a_sp13')
        self.assertTrue(ret_json["primary_list"]["list_exists"])
        self.assertEqual(len(ret_json['secondary_lists']), 21)

    def test_get_email_lists_by_term(self):
        now_request = get_request()
        get_request_with_user('bill', now_request)
        ret_json = get_email_lists_by_term(Term(year=2013, quarter='spring'))
        self.assertEqual(ret_json['year'], 2013)
        self.assertEqual(ret_json['quarter'], "spring")
        self.assertEqual(len(ret_json['email_lists']), 2)
        list1 = ret_json['email_lists'][0]
        self.assertEqual(list1["course_abbr"], "TRAIN")
        self.assertEqual(list1["course_number"], "101")
        self.assertEqual(list1["section_id"], "A")
        self.assertEqual(list1["primary_list"]['list_address'],
                         'train101a_sp13')
        self.assertTrue(list1["primary_list"]['list_exists'])
        self.assertEqual(list1["is_primary"], True)
        self.assertEqual(len(list1["secondary_lists"]), 0)
        self.assertEqual(list1["has_multi_secondaries"], False)

        list2 = ret_json['email_lists'][1]
        self.assertEqual(list2["course_abbr"], "ESS")
        self.assertEqual(list2["has_multi_secondaries"], False)
        self.assertEqual(list2["is_primary"], True)
        self.assertEqual(list2["primary_list"]['list_address'],
                         'ess102a_sp13')
        self.assertFalse(list2["primary_list"]['list_exists'])
        self.assertEqual(len(list2["secondary_lists"]), 1)
        self.assertTrue(list2["secondary_lists"][0]["list_exists"])
        self.assertEqual(list2["secondary_lists"][0]["list_address"],
                         'ess102ab_sp13')
