from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # return  HttpResponse("Welcome to Planner.")
    return render(request, "reminders/home.html")
