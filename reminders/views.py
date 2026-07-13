from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReminderForm
from .models import Reminder
from django.views.generic import UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def home(request):
    # return  HttpResponse("Welcome to Planner.")
    reminders = request.user.reminders.all()
    return render(request, 
                  "reminders/home.html",
                  { "reminders": reminders }
                  )

@login_required
def create_reminder(request):
    if (request.method == "POST"):
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            return redirect('home')
    else: 
        form = ReminderForm()
    return render(
        request,
       "reminders/create.html",
        { "form": form }
    )

class ReminderUpdateView(UpdateView, LoginRequiredMixin):
    model = Reminder
    form_class = ReminderForm
    template_name = "reminders/update.html"
    success_url = reverse_lazy('home')
    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)

class ReminderDeleteView(DeleteView, LoginRequiredMixin):
    model = Reminder
    template_name = "reminders/delete.html"
    success_url = reverse_lazy('home')
    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)
    
class ReminderDetailView(DeleteView, LoginRequiredMixin):
    model = Reminder
    template_name = "reminders/detail.html"
    success_url = reverse_lazy("home")
    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)
