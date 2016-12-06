from hc.api.models import Check
from hc.test import BaseTestCase


class NagTestCase(BaseTestCase):

    def setUp(self):
        super(NagTestCase, self).setUp()
        self.check = Check(user=self.alice, status="down")
        self.check.save()

    def test_it_updates_nag_state(self):
        url = "/checks/%s/nag/" % self.check.code
        payload = {"nag_timeout": 3600, "nag_enabled": 'on'}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, data=payload)
        self.assertRedirects(response, "/checks/")

        self.check.refresh_from_db()
        self.assertEqual(self.check.nag_timeout, 3600)
        self.assertTrue(self.check.nag_enabled)
