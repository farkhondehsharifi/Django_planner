from django.contrib import admin
from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "time", "user")
    list_filter = ("title", "user")
    search_fields = ("date", "title", "description")
    ordering = ("-date",)