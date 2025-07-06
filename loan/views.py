import json
from django.contrib import messages
from http.client import responses, error
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoanPaymentForm, BankForm
from .tete import Bank, Loans

class BankView(View):
    template_name = "loan/bank.html"
    def get(self, request):

        form = BankForm()
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
        form = BankForm(request.POST)
        if form.is_valid():
            loan_amount = float(form.cleaned_data['loan_amount'])
            int_rate = float(form.cleaned_data['int_rate'])
            months = int(form.cleaned_data['months'])

            data = Bank(loan_amount, int_rate, months)
            result = data.bank_loan()  # This should be a list of dicts
            request.session['result'] = json.dumps(result)
            return redirect(request.path)

        messages.error(request, "Entrada incorrecta")
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

            if loan_amount * (loan_interest/100) >= month_pay: #This is to avoid infinite loan, the interest*loan amount is more that the mon pay it will never ends
                                                                #and this could kill the server.
                form.add_error(None, ('El pago mensual es insuficiente, ya que es igual o menor '
                                      'al interés generado. Esto provocaría una deuda interminable. '
                                      'Intenta con un pago mensual mayor al interés del préstamo para que se pueda '
                                      'finalizar el pago.')) #Displaying error message if pre applied
                return render(request, self.template_name, {'form': form})

            else:
                data = Loans(loan_amount, month_pay, loan_interest)
                result = data.pay_loan_amount()  # This should be a list of dicts
                request.session['result'] = json.dumps(result)
                return redirect(request.path)

        # If form is invalid in general
        return render(request, self.template_name, {'form': form})




















