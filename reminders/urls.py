from django.urls import path
from . import views
from.views import ReminderUpdateView, ReminderDeleteView, ReminderDetailView

urlpatterns = [
    path("", views.home, name="home"),
    path("reminders/create/",
         views.create_reminder,
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