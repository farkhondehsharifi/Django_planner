from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from reminders.models import Reminder
from accounts.tests.factories import UserFactory
from reminders.tests.factories import ReminderFactory

class ReminderOwnershipTests(TestCase):
    def test_user_cannot_access_other_users_reminder_detail(self):
        owner = UserFactory()
        other_user = UserFactory()
        reminder = ReminderFactory(user=owner)

        self.client.force_login(other_user)
        response = self.client.get(reverse("reminder_detail", kwargs={"pk": reminder.pk}))

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_update_other_users_reminder(self):
        owner = UserFactory()
        other_user = UserFactory()
        reminder = ReminderFactory(user=owner)

        self.client.force_login(other_user)
        response = self.client.get(reverse("update_reminder", kwargs={"pk": reminder.pk}))

        self.assertEqual(response.status_code, 404)
