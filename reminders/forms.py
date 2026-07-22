from datetime import datetime

from django import forms
from django.utils import timezone

from .models import Reminder


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = [
            "title",
            "date",
            "time",
            "color",
            "description",
        ]

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if date and time:
            reminder_datetime = timezone.make_aware(
                datetime.combine(date, time))
            if reminder_datetime <= timezone.now():
                raise forms.ValidationError(
                    "Reminder date and time cannot be in the past")

        return cleaned_data
