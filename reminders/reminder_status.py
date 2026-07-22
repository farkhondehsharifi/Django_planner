from django.db import models

class ReminderStatus(models.TextChoices):
        PENDING = "PENDING"
        QUEUED = "QUEUED"
        SENT = "SENT"
        FAILED = "FAILED"