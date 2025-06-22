from django.urls import path
from . import views
from .views import BankView

app_name = "loan"
urlpatterns = [
    path("bank", BankView.as_view(), name="bank"),
    path("no_bank", views.no_bank, name="no_bank"),

]