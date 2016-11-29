from hc.api.models import Check
from hc.test import BaseTestCase


class SwitchTeamTestCase(BaseTestCase):
    def test_it_switches(self):
        check = Check(user=self.alice, name="This belongs to Alice")
        check.save()

        self.client.login(username="bob@example.org", password="password")
        url = "/accounts/switch_team/%s/" % self.alice.username
        response = self.client.get(url, follow=True)

        self.assertContains(response, 'This belongs to Alice')

    def test_it_checks_team_membership(self):
        self.client.login(username="charlie@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        response = self.client.get(url)

        self.assertEqual(403, response.status_code)

    def test_it_switches_to_own_team(self):
        self.client.login(username="alice@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        response = self.client.get(url, follow=True)

        self.assertEqual(200, response.status_code)
