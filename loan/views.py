import json
from django.contrib import messages
from http.client import responses, error
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoanPaymentForm
from .tete import Bank, Loans

class BankView(View):
    def get(self, request):
        result_json = request.session.pop('result', None)
        result = json.loads(result_json) if result_json else None
        return render(request, "loan/bank.html", {'result': result})

    def post(self, request):
        try:
            loan_amount = float(request.POST.get('loan_amount'))
            loan_rate = float(request.POST.get('loan_rate'))
            loan_months = float(request.POST.get('loan_months'))
        except (TypeError, ValueError):
            messages.error(request, "Entrada incorrecta")
            return redirect(request.path)

        data = Bank(loan_amount, loan_rate, loan_months)
        result = data.bank_loan()  # This should be a list of dicts
        request.session['result'] = json.dumps(result)
        return redirect(request.path)

class NoBankView(View):
    template_name = "loan/no_bank.html"


    def get(self, request):
        form = LoanPaymentForm()
        result_json = request.session.pop('result', None)

        try:
            result = json.loads(result_json) if result_json else None
        except json.JSONDecodeError:
            result = None
            messages.error(request, "Error al leer los resultados anteriores.")

        return render(request, self.template_name, {
            'form': form,
            'result': result
        })

    def post(self, request):
        form = LoanPaymentForm(request.POST)

        if form.is_valid():
            loan_amount = float(form.cleaned_data['loan_amount'])
            month_pay = float(form.cleaned_data['month_pay'])
            loan_interest = float(form.cleaned_data['loan_interest'])

            if loan_amount * loan_interest >= month_pay:
                form.add_error(None, ('El pago mensual es insuficiente, ya que es igual o menor '
                                      'al interés generado. Esto provocaría una deuda interminable. '
                                      'Intenta con un pago mensual mayor al interés del préstamo para que se pueda '
                                      'finalizar el pago.'))
                return render(request, self.template_name, {'form': form})

            else:
                data = Loans(loan_amount, month_pay, loan_interest)
                result = data.pay_loan_amount()  # This should be a list of dicts
                request.session['result'] = json.dumps(result)
                return redirect(request.path)

        # If form is invalid in general
        return render(request, self.template_name, {'form': form})




















