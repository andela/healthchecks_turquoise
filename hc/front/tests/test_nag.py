from datetime import timedelta

from hc.api.models import Check
from hc.test import BaseTestCase
from django.utils import timezone


class NagTestCase(BaseTestCase):

    def setUp(self):
        super(NagTestCase, self).setUp()
        self.check = Check(user=self.alice, status="down")
        self.check.last_ping = timezone.now() - timedelta(days=1)
        self.check.save()

    def test_it_updates_nag_state(self):
        url = "/checks/%s/nag/" % self.check.code
        payload = {"nag_timeout": 3600, "nag_enabled": 'True'}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, data=payload)
        self.assertRedirects(response, "/checks/")

        self.check.refresh_from_db()
        self.assertEqual(self.check.nag_timeout.total_seconds(), 3600)
        self.assertTrue(self.check.nag_enabled)

    def test_it_disables_nag(self):
        url = "/checks/%s/nag/" % self.check.code
        payload = {"nag_timeout": 3600}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, data=payload)
        self.assertRedirects(response, "/checks/")

        self.check.refresh_from_db()

        self.assertFalse(self.check.nag_enabled)
