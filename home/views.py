from http.client import responses
from django.http import HttpResponse
from django.shortcuts import render, redirect

def home(request):
    return render(request, "home/main_page.html")

def about(request):
    response = render(request, "home/about.html")
    return response

def contact(request):
    return render(request, "home/contact.html")

def more(request):
    return render(request, "home/more.html")