from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from hc.api.models import Check


class CheckModelTestCase(TestCase):

    def test_it_strips_tags(self):
        check = Check()

        check.tags = " foo  bar "
        self.assertEquals(check.tags_list(), ["foo", "bar"])
        ### Repeat above test for when check is an empty string
        check.tags = ""
        self.assertEquals(check.tags_list(), [])

    def test_status_works_with_grace_period(self):
        check = Check()

        check.status = "up"
<<<<<<< HEAD
        check.last_ping = timezone.now() - timedelta(days=2, minutes=30)

        ### The above 2 asserts fail. Make them pass
        self.assertNotEqual(check.get_status(), "up")
=======
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)

        ### The above 2 asserts fail. Make them pass
        # option: 1
        if check.in_grace_period():
            self.assertEqual(check.get_status(), "up")
        else:
            self.assertEqual(check.get_status(), "down")
        # option: 2
        # self.assertFalse(check.in_grace_period()) 
        # self.assertNotEqual(check.get_status(), "up")
>>>>>>> origin/ft-api-tests-133846503

    def test_paused_check_is_not_in_grace_period(self):
        check = Check()

        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        self.assertTrue(check.in_grace_period())

        check.status = "paused"
        self.assertFalse(check.in_grace_period())

    ### Test that when a new check is created, it is not in the grace period
    def test_new_check_is_not_in_grace_period(self):
        check = Check()

<<<<<<< HEAD
        check.status = "new"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
=======
        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        self.assertTrue(check.in_grace_period())

        check.status = "paused"
>>>>>>> origin/ft-api-tests-133846503
        self.assertFalse(check.in_grace_period())