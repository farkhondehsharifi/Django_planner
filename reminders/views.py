from django.shortcuts import render
from django.http import HttpResponse
from .models import Reminder
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # return  HttpResponse("Welcome to Planner.")
    reminders = request.user.reminders.all()
    return render(request, 
                  "reminders/home.html",
                  { "reminders": reminders }
                  )
