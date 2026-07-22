from datetime import timedelta

from django.core import mail
from django.test import TestCase
from django.utils import timezone

from reminders.models import Reminder
from reminders.reminder_status import ReminderStatus
from reminders.tasks import send_reminder_email
from accounts.tests.factories import UserFactory
from reminders.tests.factories import ReminderFactory


class ReminderTaskTests(TestCase):
    def test_send_reminder_email_sends_mail_for_valid_user(self):
        reminder = ReminderFactory()
        send_reminder_email(reminder.id)

        self.assertEqual(len(mail.outbox), 1)
        reminder.refresh_from_db()
        self.assertEqual(reminder.status, ReminderStatus.SENT)

    def test_send_reminder_email_skips_when_user_email_is_empty(self):
        reminder = ReminderFactory(user=UserFactory(email=""))
        send_reminder_email(reminder.id)

        self.assertEqual(len(mail.outbox), 0)
        reminder.refresh_from_db()
        self.assertEqual(reminder.status, ReminderStatus.FAILED)