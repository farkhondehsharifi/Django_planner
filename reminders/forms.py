from .models import Reminder
from django import forms

class ReminderForm(forms.ModelForm):

    class Meta:
        model = Reminder
        fields = [
            "title",
            "date",
            "time",
            "color",
            "description"
        ] 