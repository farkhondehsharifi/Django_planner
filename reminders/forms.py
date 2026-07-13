from .models import Reminder
from django import forms
from django.utils import timezone

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

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError("Reminder date cannot be in the past")
        return date