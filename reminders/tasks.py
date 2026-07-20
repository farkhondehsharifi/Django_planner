from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Reminder

@shared_task
def check_due_reminders():
    now = timezone.localtime()
    reminders = Reminder.objects.filter(
        date=now.date(),
        time__lte=now.time(),
        sent=False,
        user__email__isnull=False
    ).exclude(
        user__email=""
    )
    for reminder in reminders:
        send_reminder_email.delay(reminder.id)

@shared_task
def send_reminder_email(reminder_id):
    reminder = Reminder.objects.get(id=reminder_id)
    send_mail(
        subject=f"Reminder:{reminder.title}",
        message=f"""
            Title: {reminder.title},
            Date: {reminder.date},
            Time: {reminder.time},
            Description: {reminder.description},
        """,
    from_email=None,
    recipient_list=[reminder.user.email]
    )
    reminder.sent=True
    reminder.save()
