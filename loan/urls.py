from django.urls import path
from . import views

app_name = "loan"
urlpatterns = [
    path("bank", views.bank, name="bank"),
    path("no_bank", views.no_bank, name="no_bank"),

]