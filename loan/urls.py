from django.urls import path

from .views import BankView, NoBankView, RegisterLoanView, NoBankCreateView, BankListView, \
    NoBankDetailUpdateView, BankCreateView, BankLoanDetailView, BankLoanDeleteView, NoBankLoanDeleteView, \
    BankLoanDetailPay


app_name = "loan"
urlpatterns = [
    path("bank", BankView.as_view(), name="bank"),
    path("nobank", NoBankView.as_view(), name="no_bank"),
    path("register", RegisterLoanView.as_view(), name="register_loan"),

    #Loans urls...
    path("no_bank/create", NoBankCreateView.as_view(), name="create_nobank"),
    path("bank/create", BankCreateView.as_view(), name="create_bank"),
    path("banks/list", BankListView.as_view(), name="bank_list"),

    #bank loan details...
    path("bank/<int:pk>", BankLoanDetailView.as_view(), name="bank_detail"),
    path("bank/<int:pk>/delete", BankLoanDeleteView.as_view(), name="bank_delete"),
    path("bank/detail/pay/<int:pk>", BankLoanDetailPay.as_view(), name="bank_detail_pay"),

    #no_loan details and update...
    path("no_bank/<int:pk>", NoBankDetailUpdateView.as_view(), name="no_bank_detail"),
    path("no_bank/<int:pk>/delete", NoBankLoanDeleteView.as_view(), name="no_bank_delete" ),

]