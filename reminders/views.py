from django.shortcuts import render
from django.http import HttpResponse
from .models import Reminder

def home(request):
    # return  HttpResponse("Welcome to Planner.")
    reminders = Reminder.objects.all()
    return render(request, 
                  "reminders/home.html",
                  { "reminders": reminders }
                  )
