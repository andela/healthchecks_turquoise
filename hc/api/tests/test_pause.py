from hc.api.models import Check
from hc.test import BaseTestCase
from django.test import RequestFactory


class PauseTestCase(BaseTestCase):

    def test_it_works(self):
        check = Check(user=self.alice, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        resp = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        ### Assert the expected status code and check's status
        check.refresh_from_db()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(check.status, 'paused')

    def test_it_validates_ownership(self):
        check = Check(user=self.bob, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        resp = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        self.assertEqual(resp.status_code, 400)

        ### Test that it only allows post requests
        # Reference -->>> https://docs.djangoproject.com/en/dev/topics/testing/advanced/
        req_factory = RequestFactory()
        req = req_factory.post(url, "", content_type="application/json", HTTP_X_API_KEY="abc")
        self.assertEqual(req.method, 'POST')
