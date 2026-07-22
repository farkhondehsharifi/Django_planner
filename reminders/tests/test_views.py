from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from reminders.models import Reminder
from accounts.tests.factories import UserFactory
from reminders.tests.factories import ReminderFactory


class ReminderViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.future = timezone.now() + timedelta(days=1)
        self.create_payload = {
            "title": "New Reminder",
            "date": self.future.date().isoformat(),
            "time": self.future.time().strftime("%H:%M"),
            "color": "#00ff00",
            "description": "Remember to finish this task.",
        }

    def test_home_view_requires_login(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_home_view_shows_only_current_user_reminders(self):
        self.client.force_login(self.user)

        ReminderFactory(user=self.user, title="Mine")
        ReminderFactory(user=self.other_user, title="Not mine")

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        reminders = list(response.context["reminders"])
        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0].title, "Mine")

    def test_create_view_post_creates_reminder_for_logged_in_user(self):
        self.client.force_login(self.user)

        with patch("reminders.models.Reminder.schedule") as schedule_mock:
            response = self.client.post(
                reverse("create_reminder"),
                data=self.create_payload,
                follow=True,
            )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(Reminder.objects.count(), 1)
        reminder = Reminder.objects.get()
        self.assertEqual(reminder.user, self.user)
        self.assertEqual(reminder.title, self.create_payload["title"])
        schedule_mock.assert_called_once()

    def test_detail_view_shows_owned_reminder(self):
        self.client.force_login(self.user)
        reminder = ReminderFactory(user=self.user, title="Detail Reminder")

        response = self.client.get(
            reverse("reminder_detail", kwargs={"pk": reminder.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["reminder"].pk, reminder.pk)
        self.assertEqual(response.context["reminder"].title, "Detail Reminder")

    def test_update_view_post_updates_reminder_and_reschedules_when_datetime_changes(self):
        self.client.force_login(self.user)
        reminder = ReminderFactory(
            user=self.user,
            title="Original Title",
            date=(timezone.now() + timedelta(days=2)).date(),
            time=(timezone.now() + timedelta(days=2)).time(),
        )

        updated_future = timezone.now() + timedelta(days=3)
        payload = {
            "title": "Updated Title",
            "date": updated_future.date().isoformat(),
            "time": updated_future.time().strftime("%H:%M"),
            "color": reminder.color,
            "description": "Updated description",
        }

        with patch("reminders.models.Reminder.revoke") as revoke_mock, patch(
            "reminders.models.Reminder.schedule"
        ) as schedule_mock:
            response = self.client.post(
                reverse("update_reminder", kwargs={"pk": reminder.pk}),
                data=payload,
            )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        reminder.refresh_from_db()
        self.assertEqual(reminder.title, "Updated Title")
        revoke_mock.assert_called_once()
        schedule_mock.assert_called_once()

    def test_delete_view_post_deletes_reminder_for_owner(self):
        self.client.force_login(self.user)
        reminder = ReminderFactory(user=self.user)

        with patch("reminders.models.Reminder.revoke") as revoke_mock:
            response = self.client.post(
                reverse("delete_reminder", kwargs={"pk": reminder.pk}),
            )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(Reminder.objects.filter(pk=reminder.pk).exists())
        revoke_mock.assert_called_once()
