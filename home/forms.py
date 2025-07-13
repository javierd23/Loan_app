from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class SingUpForm(UserCreationForm):
    model = User
    class Meta:

        fields = ['username','first_name', 'last_name', 'email' '<PASSWORD>', '<PASSWORD>', ]

