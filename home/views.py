from http.client import responses

from django.urls import reverse

from .forms import SingUpForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View


def home(request):
    return render(request, "home/main_page.html")

def about(request):
    response = render(request, "home/about.html")
    return response

def contact(request):
    return render(request, "home/contact.html")

def more(request):
    return render(request, "home/more.html")


#Let's get the user a sing up on here.

class SingUpView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "home/sing_up.html", {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect(reverse('home:home'))
        else:
            return render(request, "home/sing_up.html", {'form': form})
