from .forms import ReminderForm
from .models import Reminder
from django.views.generic import UpdateView, DeleteView, DetailView, CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import UserReminderMixin
from django.db.models import Q
from django.utils import timezone


class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = "reminders/home.html"
    context_object_name = 'reminders'
    paginate_by = 2
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        status = self.request.GET.get('status')
        now = timezone.now()
        today = now.date()
        current_time = now.time()
        if status == 'completed':
            queryset = queryset.filter(Q(date__lt=today) | (Q(date=today) & Q(time__lt=current_time)))
        elif status == 'today':
            queryset = queryset.filter(Q(date=today) | Q(time__gte=current_time))
        elif status == 'upcoming':
            queryset = queryset.filter(Q(date__gt=today))
        return queryset.order_by(
            "date",
            "time"
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        context['current_status'] = self.request.GET.get("status", '')
        return context

class ReminderCreateView(LoginRequiredMixin, CreateView):
    model = Reminder
    form_class = ReminderForm
    template_name = "reminders/create.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        reminder = self.object
        reminder.schedule()
        return response

class ReminderUpdateView(LoginRequiredMixin, UserReminderMixin, UpdateView):
    model = Reminder
    form_class = ReminderForm
    template_name = "reminders/update.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        reminder = self.get_object()
        old_date = reminder.date
        old_time = reminder.time

        response = super().form_valid(form)

        if old_date != self.object.date or old_time != self.object.time:
            self.object.revoke()
            self.object.schedule()

        return response

class ReminderDeleteView(LoginRequiredMixin, UserReminderMixin, DeleteView):
    model = Reminder
    template_name = "reminders/delete.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        reminder = self.object
        reminder.revoke()
        return super().form_valid(form)
    
class ReminderDetailView(LoginRequiredMixin, UserReminderMixin, DetailView ):
    model = Reminder
    template_name = "reminders/detail.html"
    success_url = reverse_lazy("home")
