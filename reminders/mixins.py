from .models import Reminder

class UserReminderMixin:
    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user).order_by(
            "date",
            "time"
        )