from django import forms

class LoanPaymentForm(forms.Form):
    loan_amount = forms.DecimalField(label="Monto del Préstamo", max_digits=12)
    month_pay = forms.DecimalField(label="Monto", max_digits=12)
    loan_interest = forms.DecimalField(label="Interés del Préstamo", max_digits=12)