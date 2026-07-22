from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Reminder
from .reminder_status import ReminderStatus
from django.conf import settings

# @shared_task
# def check_due_reminders():
#     now = timezone.localtime()
#     reminders = Reminder.objects.filter(
#         date=now.date(),
#         time__lte=now.time(),
#         sent=False,
#         user__email__isnull=False
#     ).exclude(
#         user__email=""
#     )
#     for reminder in reminders:
#         send_reminder_email.delay(reminder.id)

@shared_task
def send_reminder_email(reminder_id):
    reminder = Reminder.objects.select_related('user').get(id=reminder_id)
    if not reminder.user.email:
        reminder.status=ReminderStatus.FAILED
        reminder.save(update_fields=['status'])
        return
    send_mail(
        subject=f"Reminder:{reminder.title}",
        message = f"""
                Hello {reminder.user.first_name or reminder.user.username},

                This is your reminder.

                Title:
                {reminder.title}

                Date:
                {reminder.date}

                Time:
                {reminder.time}

                Description:
                {reminder.description}

                Have a productive day!

                Planner
            """,
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[reminder.user.email]
    )
    reminder.status=ReminderStatus.SENT
    reminder.save(update_fields=['status'])
