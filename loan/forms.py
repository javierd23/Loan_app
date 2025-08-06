from django import forms
from .models import NoBankLoan

class LoanPaymentForm(forms.Form):
    loan_amount = forms.DecimalField(label="Monto del Préstamo", max_digits=12)
    month_pay = forms.DecimalField(label="Monto", max_digits=12)
    loan_interest = forms.DecimalField(label="Interés del Préstamo", max_digits=12)

class BankForm(forms.Form):
    loan_amount = forms.DecimalField(label="Monto del préstamo", max_digits=12)
    int_rate = forms.DecimalField(label="Interés anual", max_digits=12)
    months = forms.DecimalField(label="Cuotas", max_digits=12)


class NobanForm(forms.ModelForm):
    class Meta:
        model = NoBankLoan
        exclude = ['user']
