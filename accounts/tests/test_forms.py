from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import SignupForm
from accounts.tests.factories import UserFactory

class SignupFormTests(TestCase):
    def test_signup_form_rejects_weak_password(self):
        form = SignupForm(
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "123",
                "password2": "123",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("password", str(form.errors))

    def test_signup_form_rejects_duplicate_username(self):
        UserFactory(username="existinguser")

        form = SignupForm(
            data={
                "username": "existinguser",
                "email": "another@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_signup_form_rejects_mismatched_passwords(self):
        form = SignupForm(
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPass123!",
                "password2": "DifferentPass123!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
