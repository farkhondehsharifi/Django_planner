from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from reminders.models import Reminder
from accounts.tests.factories import UserFactory
from reminders.tests.factories import ReminderFactory


class ReminderRescheduleTests(TestCase):
    def test_update_without_changing_date_or_time_does_not_reschedule(self):
        user = UserFactory()
        self.client.force_login(user)

        future_time = timezone.now() + timedelta(days=1)
        reminder = ReminderFactory(
            user=user,
            date=future_time.date(),
            time=future_time.time()
        )
        reminder.schedule()
        original_task_id = reminder.task_id

        response = self.client.post(
            reverse("update_reminder", kwargs={"pk": reminder.pk}),
            {
                "title": "Updated title",
                "date": future_time.date(),
                "time": future_time.time(),
                "color": "#123456",
                "description": "Updated description",
            },
        )

        self.assertEqual(response.status_code, 302)
        reminder.refresh_from_db()
        self.assertEqual(reminder.task_id, original_task_id)

    def test_update_with_new_date_or_time_reschedules(self):
        user = UserFactory()
        self.client.force_login(user)

        future_time = timezone.now() + timedelta(days=1)
        reminder = ReminderFactory(
            user=user,
            date=future_time.date(),
            time=future_time.time()
        )
        reminder.schedule()
        old_task_id = reminder.task_id

        new_future_time = future_time + timedelta(days=2)
        response = self.client.post(
            reverse("update_reminder", kwargs={"pk": reminder.pk}),
            {
                "title": "Updated title",
                "date": new_future_time.date(),
                "time": new_future_time.time(),
                "color": "#123456",
                "description": "Updated description",
            },
        )

        self.assertEqual(response.status_code, 302)
        reminder.refresh_from_db()
        self.assertNotEqual(reminder.task_id, old_task_id)
