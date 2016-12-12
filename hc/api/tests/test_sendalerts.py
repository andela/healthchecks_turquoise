from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch
from datetime import timedelta as td


class SendAlertsTestCase(BaseTestCase):

    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_handles_few(self, mock):
        yesterday = timezone.now() - timedelta(days=1)
        names = ["Check %d" % d for d in range(0, 10)]

        for name in names:
            check = Check(user=self.alice, name=name)
            check.alert_after = yesterday
            check.status = "up"
            check.save()

        result = Command().handle_many()
        assert result, "handle_many should return True"

        handled_names = []
        for args, kwargs in mock.call_args_list:
            handled_names.append(args[0].name)

        assert set(names) == set(handled_names)
        ### The above assert fails. Make it pass

    def test_it_handles_grace_period(self):
        check = Check(user=self.alice, status="up")
        # 1 day 30 minutes after ping the check is in grace period:
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        check.save()

        # Expect no exceptions--
        Command().handle_one(check)

    ### Assert when Command's handle many that when handle_many should return True

    def test_it_handles_check_in_nag_state(self):
        check = Check(user=self.alice, status="down")
        check.last_ping = timezone.now() - timedelta(days=1, hours=13)
        check.get_status()
        check.save()

        check.refresh_from_db()
        self.assertEqual("nag", check.get_status())

    def test_alerts_work(self):
        check = Check(user=self.alice, status="up")
        check.timeout = td(minutes=5)
        check.grace = td(minutes=2)
        check.nag_timeout = td(minutes=1)
        check.save()

        check.refresh_from_db()
        check.last_ping = timezone.now() - td(minutes=7, seconds=60)
        check.save()

        check.refresh_from_db()

        print(check.last_nag.isoformat())

