from django.core import mail

from hc.accounts.models import Member
from hc.api.models import Check
from hc.test import BaseTestCase


class ProfileTestCase(BaseTestCase):
    def test_it_sends_set_password_link(self):
        self.client.login(username="alice@example.org", password="password")
        form_data = {"set_password": "1"}

        response = self.client.post("/accounts/profile/", form_data)
        self.assertEqual(302, response.status_code)

        # profile.token should be set now
        self.alice.profile.refresh_from_db()
        token = self.alice.profile.token

        self.assertIsNotNone(token)

        # check content of email sent
        self.assertTrue(len(mail.outbox) > 0)
        self.assertEqual('Set password on healthchecks.io', mail.outbox[0].subject)
        self.assertIn(self.alice.email, mail.outbox[0].to)
        self.assertIn("Here's a link to set a password for your account on healthchecks.io", mail.outbox[0].body)

    def test_it_sends_report(self):
        check = Check(name="Test Check", user=self.alice)
        check.save()

        self.alice.profile.send_report()

        # check content of email sent
        self.assertTrue(len(mail.outbox) > 0)

        self.assertIn("alice@example.org", mail.outbox[0].to)
        self.assertIn("Monthly Report", mail.outbox[0].subject)
        self.assertIn("This is a monthly report sent by healthchecks.io", mail.outbox[0].body)

    def test_it_adds_team_member(self):
        self.client.login(username="alice@example.org", password="password")
        form_data = {"invite_team_member": "1", "email": "frank@example.org"}

        response = self.client.post("/accounts/profile/", form_data)
        self.assertContains(response, "Invitation to {} sent!".format("frank@example.org"))

        member_emails = set()
        for member in self.alice.profile.member_set.all():
            member_emails.add(member.user.email)

        # check existence of the member emails
        self.assertTrue("frank@example.org" in member_emails)
        self.assertTrue("bob@example.org" in member_emails)

        # check content of the email sent
        self.assertTrue(len(mail.outbox) > 0)

        self.assertIn('frank@example.org', mail.outbox[0].to)
        self.assertIn("You have been invited to join {} on ".format("alice@example.org"), mail.outbox[0].subject)
        self.assertIn("You will be able to manage their existing monitoring checks and set up new", mail.outbox[0].body)

    def test_add_team_member_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")
        form_data = {"invite_team_member": "1", "email": "frank@example.org"}

        response = self.client.post("/accounts/profile/", form_data)
        self.assertEqual(403, response.status_code)

    def test_it_removes_team_member(self):
        self.client.login(username="alice@example.org", password="password")
        form_data = {"remove_team_member": "1", "email": "bob@example.org"}

        response = self.client.post("/accounts/profile/", form_data)
        self.assertContains(response, "{} removed from team!".format("bob@example.org"))

        self.assertEqual(Member.objects.count(), 0)
        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, None)

    def test_it_sets_team_name(self):
        self.client.login(username="alice@example.org", password="password")
        form_data = {"set_team_name": "1", "team_name": "Alpha Team"}

        response = self.client.post("/accounts/profile/", form_data)
        self.assertContains(response, "Team Name updated!")

        self.alice.profile.refresh_from_db()
        self.assertEqual(self.alice.profile.team_name, "Alpha Team")

    def test_set_team_name_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")
        form_data = {"set_team_name": "1", "team_name": "Charlies Team"}

        response = self.client.post("/accounts/profile/", form_data)
        self.assertEqual(403, response.status_code)

    def test_it_switches_to_own_team(self):
        self.client.login(username="bob@example.org", password="password")

        self.client.get("/accounts/profile/")

        # After visiting the profile page, team should be switched back
        # to user's default team.
        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, self.bobs_profile)

    def test_it_shows_badges(self):
        self.client.login(username="alice@example.org", password="password")
        Check.objects.create(user=self.alice, tags="foo a-B_1  baz@")
        Check.objects.create(user=self.bob, tags="bobs-tag")

        response = self.client.get("/accounts/profile/")
        self.assertContains(response, "foo.svg")
        self.assertContains(response, "a-B_1.svg")

        # Expect badge URLs only for tags that match \w+
        self.assertNotContains(response, "baz@.svg")

        # Expect only Alice's tags
        self.assertNotContains(response, "bobs-tag.svg")

    def test_it_creates_api_key(self):
        self.client.login(username="alice@example.org", password="password")
        form_data = {'create_api_key': ''}

        # create api key
        response = self.client.post("/accounts/profile/", form_data)
        self.assertContains(response, "The API key has been created!")

        # check api key in db
        self.alice.refresh_from_db()
        self.assertIsNotNone(self.alice.profile.api_key)

        # revoke api key
        form_data = {'revoke_api_key': ''}

        response = self.client.post("/accounts/profile/", form_data)
        self.assertContains(response, "The API key has been revoked!")
