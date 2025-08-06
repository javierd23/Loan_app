from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import login


from .forms import SingUpForm

from .forms import ProfileCreate

from .models import UserProfile
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from django.views import View



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

#user profile view...
class ProfileView(LoginRequiredMixin, View):
    template_name = "accounts/user_profile.html"

    def get(self, request, username):
        user_obj = get_object_or_404(User, username=username)

        try:
            profile = UserProfile.objects.get(user=user_obj)
            context = {"user_obj": user_obj, "profile": profile}
            return render(request, self.template_name, context)

        except UserProfile.DoesNotExist:
            return redirect(reverse('accounts:settings', args=[username]))


class ProfileUpdateOrCreateView(LoginRequiredMixin, View):
    """
        A view that handles creating a new UserProfile or updating an existing one.
        This view is more flexible than using separate CreateView and UpdateView.
    """

    template_name = "accounts/user_settings.html"


    def get(self, request, *args, **kwargs):

        try:
            profile = request.user.profiles
            form = ProfileCreate(instance=profile)

        except UserProfile.DoesNotExist:
            form = ProfileCreate()

        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            profile = request.user.profiles
            form = ProfileCreate(request.POST, request.FILES, instance=profile)
        except UserProfile.DoesNotExist:
            form = ProfileCreate(request.POST, request.FILES)


        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect(reverse_lazy('accounts:profile', args=[request.user.username]))

        context = {'form': form}
        return render(request, self.template_name, context)


















