from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import SingUpForm


class SingUpView(View):
    def get(self, request):
        form = SingUpForm()
        return render(request, "home/sing_up.html", {'form': form})

    def post(self, request):
        form = SingUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect(reverse('home:home'))
        else:
            return render(request, "home/sing_up.html", {'form': form})