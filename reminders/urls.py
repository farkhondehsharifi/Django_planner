from django.urls import path
from . import views
from.views import ReminderUpdateView, ReminderDeleteView, ReminderDetailView, ReminderCreateView, ReminderListView

urlpatterns = [
    path(
        "",
        ReminderListView.as_view(),
        name="home"
    ),
    path(
        "reminders/create/",
         ReminderCreateView.as_view(),
         name="create_reminder"
         ),
        path(
            "<int:pk>/edit/",
            ReminderUpdateView.as_view(),
            name="update_reminder"
        ),
        path(
            "<int:pk>/destroy/",
            ReminderDeleteView.as_view(),
            name="delete_reminder"
        ),
        path(
            "<int:pk>/",
            ReminderDetailView.as_view(),
            name="reminder_detail"
        )
]