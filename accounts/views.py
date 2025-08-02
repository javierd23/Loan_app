from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.auth import login
from rest_framework.reverse import reverse_lazy

from .forms import SingUpForm

from .forms import ProfileCreate

from .models import UserProfile
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

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
        user = get_object_or_404(User, username=username)

        try:
            profile = UserProfile.objects.get(user=user)
            context = {"user": user, "profile": profile}
            return render(request, self.template_name, context)

        except UserProfile.DoesNotExist:
            return redirect(reverse('accounts:settings', args=[username]))


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = UserProfile
    template_name = "accounts/user_settings.html"
    form_class = ProfileCreate
    success_url = "accounts:profile"

    def form_valid(self, form):
        #adding the user to the profile
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:settings', args=[self.request.user.username])

























