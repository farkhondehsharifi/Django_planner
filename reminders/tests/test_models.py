from datetime import timedelta
from unittest.mock import patch, Mock

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from reminders.models import Reminder
from reminders.reminder_status import ReminderStatus
from accounts.tests.factories import UserFactory
from reminders.tests.factories import ReminderFactory

class ReminderModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def create_reminder(self, **kwargs):
        """
        Create a reminder with sensible defaults.
        Individual tests can override any field.
        """
        
        reminder = ReminderFactory(**kwargs)
        return reminder

    @patch("reminders.tasks.send_reminder_email")
    def test_schedule_marks_reminder_queued(self, mocked_task):
        mocked_task.apply_async.return_value = Mock(id = "Task_123")

        future_time = timezone.now() + timedelta(days=1)
        reminder = self.create_reminder(
            date=future_time.date(),
            time=future_time.time(),
        )

        reminder.schedule()
        reminder.refresh_from_db()

        self.assertEqual(reminder.status, ReminderStatus.QUEUED)
        self.assertEqual(reminder.task_id, "Task_123")

    @patch("reminders.tasks.send_reminder_email")
    def test_schedule_uses_correct_eta(self, mocked_task):
        task_result = Mock()
        task_result.id = "Task_123"
        mocked_task.apply_async.return_value = task_result

        future_time = timezone.now() + timedelta(days=1)
        reminder = self.create_reminder(
            date=future_time.date(),
            time=future_time.time(),
        )

        reminder.schedule()
        reminder.refresh_from_db()

        eta = mocked_task.apply_async.call_args.kwargs["eta"].replace(
            tzinfo=None,
            microsecond=0,
        )
        self.assertEqual(eta, future_time.replace(microsecond=0, tzinfo=None))

    def test_schedule_rejects_past_datetime(self):
        past_time = timezone.now() - timedelta(minutes=5)
        reminder = self.create_reminder(
            date=past_time.date(),
            time=past_time.time()
        )

        reminder.schedule()
        reminder.refresh_from_db()

        self.assertEqual(reminder.status, ReminderStatus.FAILED)
        self.assertIsNone(reminder.task_id)

    def test_string_representation_uses_title(self):
        reminder = self.create_reminder(title="Doctor's Appointment")

        self.assertEqual(str(reminder), "Doctor's Appointment")
