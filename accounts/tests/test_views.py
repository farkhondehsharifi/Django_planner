from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountViewTests(TestCase):
    def test_signup_page_loads(self):
        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)

    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            get_user_model().objects.filter(username="newuser").exists()
        )
        self.assertEqual(response.url, "/")
