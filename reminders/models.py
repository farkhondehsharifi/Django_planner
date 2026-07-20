from django.db import models
from django.contrib.auth.models import User

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reminders")
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    color = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    sent = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title