from tempfile import template

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "home"
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about_page"),
    path("contact/", views.contact, name="contact_page"),
    path("more/", views.more, name="more_page"),
    path("feedback/", views.FeedbackCreateView.as_view(), name="feedback"),

]