from django.db import models
from django.contrib.auth.models import User
from .reminder_status import ReminderStatus
from .tasks import send_reminder_email
from django.utils import timezone
from datetime import datetime
from config.celery import app


class Reminder(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reminders")
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    color = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=ReminderStatus.choices, default=ReminderStatus.PENDING)
    task_id = models.CharField(max_length=255, null=True)

    def schedule(self):
        eta = self.get_datetime()
        if eta <= timezone.now():
            self.status = ReminderStatus.FAILED
            self.save(update_fields=["status"])
            return None

        task = send_reminder_email.apply_async(
            args=[self.id],
            eta=eta,
        )
        self.task_id = task.id
        self.status = ReminderStatus.QUEUED
        self.save(update_fields=["task_id", "status"])

    def get_datetime(self):
        return timezone.make_aware(datetime.combine(self.date, self.time))

    def revoke(self):
        if self.task_id:
            app.control.revoke(self.task_id, terminate=True)

    def __str__(self):
        return self.title
