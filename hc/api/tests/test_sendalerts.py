from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch


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
        # TODO : Test passes!!

    def test_it_handles_grace_period(self):
        check = Check(user=self.alice, status="up")
        # 1 day 30 minutes after ping the check is in grace period:
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        check.save()

        # Expect no exceptions--
        Command().handle_one(check)

    ### Assert when Command's handle many that when handle_many should return True
    # TODO: Instruction not clear
    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_handle_many_returns_true_successfully(self, mock):
        """
        handle_many in Command should return true when many alerts are
        successfully sent
        """
        last_alert_time = timezone.now() - timedelta(days = 1)

        # create many checks
        print("Mockig handle one >>>> ", mock())
        assert mock.called
        checks_names = ["Check {}".format(name) for name in range(100)]
        for name in checks_names:
            check = Check(user=self.alice, name=name)
            check.status = 'up'
            check.alert_after = last_alert_time
            check.save()
        assert Command().handle_many(), 'handle_many should return true'


