from django.urls import path

from .views import BankView, NoBankView, RegisterLoanView, NoBankGeristerCreateView, NoBankListView, NoBankDetailUpdateView


app_name = "loan"
urlpatterns = [
    path("bank", BankView.as_view(), name="bank"),
    path("nobank", NoBankView.as_view(), name="no_bank"),
    path("register", RegisterLoanView.as_view(), name="register_loan"),

    #Loans urls...
    path("no_bank/create_nobank", NoBankGeristerCreateView.as_view(), name="create_nobank"),
    path("no_bank/list", NoBankListView.as_view(), name="no_bank_list"),

    #no_loan details and update...
    path("no_bank/<int:pk>", NoBankDetailUpdateView.as_view(), name="no_bank_detail"),

]