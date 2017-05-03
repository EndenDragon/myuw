from django.test import TestCase
from django.conf import settings
from myuw.models import UserNotices
from myuw.dao.notice import get_notices_by_regid


class TestUserNotices(TestCase):
    def test_hash(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        notices = get_notices_by_regid(regid)
        notice = notices[0]
        model = UserNotices()
        hash = model.generate_hash(notice)
        self.assertEquals(hash, "fbb05e8edaf403b7c5eb5a9ac8d7cc3b")


class TestResCategoryLinks(TestCase):

    def test_affiliation(self):
        """
        Tests the affiliation format, where the affiliation tags are
        separated by '+' characters and the ugrad/grad/
        """
        link = ResCategoryLink(
            url="http://www.washington.edu/students/reg/calendar.html",
            title="Academic Calendar",
            affiliation="all+",
            category_name="Academics",
            sub_category="Registration",
            new_tab="yes"
            )

        self.assertEquals(link.get_affiliation(), "all")
        self.assertEquals(link.get_pce(), "")

        link = ResCategoryLink(
            url="http://www.washington.edu/students/reg/calendar.html",
            title="Academic Calendar",
            affiliation="ugrad+",
            category_name="Academics",
            sub_category="Registration",
            new_tab="yes"
            )

        self.assertEquals(link.get_affiliation(), "ugrad")
        self.assertEquals(link.get_pce(), "")

        link = ResCategoryLink(
            url="http://www.washington.edu/students/reg/calendar.html",
            title="Academic Calendar",
            affiliation="nm+",
            category_name="Academics",
            sub_category="Registration",
            new_tab="yes"
            )

        self.assertEquals(link.get_affiliation(), "nm")
        self.assertEquals(link.get_pce(), "")

    def test_pce(self):
        link = ResCategoryLink(
            url="http://www.washington.edu/students/reg/calendar.html",
            title="Academic Calendar",
            affiliation="all+pce",
            category_name="Academics",
            sub_category="Registration",
            new_tab="yes"
            )

        self.assertEquals(link.get_affiliation(), "all")
        self.assertEquals(link.get_pce(), "pce")
