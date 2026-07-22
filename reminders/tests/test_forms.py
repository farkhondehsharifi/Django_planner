from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from reminders.forms import ReminderForm


class ReminderFormTests(TestCase):
    def test_form_accepts_future_reminder(self):
        future_time = timezone.now() + timedelta(days=1)

        form = ReminderForm(
            data={
                "title": "Future reminder",
                "date": future_time.date(),
                "time": future_time.time(),
                "color": "#00ff00",
                "description": "Some description",
            }
        )

        self.assertTrue(form.is_valid())

    def test_form_rejects_past_reminder(self):
        past_time = timezone.now() - timedelta(minutes=5)

        form = ReminderForm(
            data={
                "title": "Past reminder",
                "date": past_time.date(),
                "time": past_time.time(),
                "color": "#00ff00",
                "description": "Some description",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "Reminder date and time cannot be in the past",
            form.non_field_errors(),
        )
