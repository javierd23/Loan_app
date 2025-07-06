from django.urls import path
from . import views
from .views import BankView, NoBankView

app_name = "loan"
urlpatterns = [
    path("bank", BankView.as_view(), name="bank"),
    path("no_bank", NoBankView.as_view(), name="no_bank"),

]