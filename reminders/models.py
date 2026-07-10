from django.db import models
from django.contrib.auth.models import User

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    color = models.CharField(max_length=30)
    description = models.TextField(blank=True)
