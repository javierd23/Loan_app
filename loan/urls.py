from django.urls import path
from . import views
from .views import BankView, NoBankView, RegisterLoanView, NoBankGeristerCreateView, NoBankListView

app_name = "loan"
urlpatterns = [
    path("bank", BankView.as_view(), name="bank"),
    path("no_bank", NoBankView.as_view(), name="no_bank"),
    path("register", views.RegisterLoanView.as_view(), name="register_loan"),

    #Loans urls...
    path("no_bank/create_nobank", NoBankGeristerCreateView.as_view(), name="create_nobank"),
    path("no_bank/list", NoBankListView.as_view(), name="no_bank_list"),

]