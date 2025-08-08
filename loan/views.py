import json
from django.contrib import messages
from http.client import responses, error

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from django.views.generic import CreateView, ListView, DetailView

from .models import NoBankLoan, BankLoan

from .forms import LoanPaymentForm, BankForm, NobanForm, BankLoanForm
from .tete import Bank, Loans, no_bank_desc_loan

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

            #Let's catch some tests on here. We do not want the user to enter more than 600 months,
            # 600 months is iqual to 50 years, this is enough not to kill the server. To avoid creative
            # enter of eg. 40,000, or something like that, it would kill the server for sure.
            if months < 1 or months > 600:
                form.add_error(None, ('No mas de 600 meses y menos de 1 mes es permitido.'))  # Displaying error message...
                return render(request, self.template_name, {'form': form})

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



#register your loan view.
class RegisterLoanView(LoginRequiredMixin, View):
    """A simple view to select the type of loan."""

    def get(self, request):
        return render(request, 'loan/register_loan.html')

#creating a No_bank loan...

class NoBankGeristerCreateView(LoginRequiredMixin, CreateView):
    template_name = "loan/nobank_loan.html"
    form_class = NobanForm
    model = NoBankLoan
    success_url = "loan/no_bank_list.html"

    def form_valid(self, form):

        no_bank = form.save(commit=False)
        no_bank.user = self.request.user
        no_bank.save()
        return super().form_valid(form)


class BankListView(LoginRequiredMixin, ListView):
    template_name = "loan/nobank_list.html"
    context_object_name = 'no_loans'

    def queryset(self, **kwargs):
        return NoBankLoan.objects.filter(user=self.request.user)

    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bank"] = BankLoan.objects.filter(user=self.request.user)
        return context


class NoBankDetailUpdateView(LoginRequiredMixin, View):
    """A view that will display the details of the loan,
       and it will also update the loan"""

    template_name = "loan/no_bank_detail.html"


    def get(self, request, pk):
        no_bank = get_object_or_404(NoBankLoan, pk=pk)
        form_bank = NobanForm(instance=no_bank, prefix='bank')
        form = LoanPaymentForm(prefix='calculator')
        result_json = request.session.pop('result', None)

        try:
            result = json.loads(result_json) if result_json else None
        except json.JSONDecodeError:
            result = None
            messages.error(request, "Error al leer los resultados anteriores.")

        context = {"no_bank": no_bank, "form": form, "form_bank": form_bank, "result": result}

        return render(request, self.template_name, context)

    def post(self, request, pk):
        no_bank = get_object_or_404(NoBankLoan, pk=pk)
        form_bank = NobanForm(request.POST, instance=no_bank, prefix='bank')

        form = LoanPaymentForm(request.POST, prefix='calculator')

        context = {
            "no_bank": no_bank,
            "form_bank": form_bank,
            "form": form
        }

        if "bank-submit" in request.POST:
            if form_bank.is_valid():

                name = form_bank.cleaned_data['name']
                payment = float(form_bank.cleaned_data['monthly_payment'])
                loan_interest = int(form_bank.cleaned_data['interest_rate'])
                loan_amount = float(form_bank.cleaned_data['loan_amount'])

                if payment < (loan_interest/100) * loan_amount:
                    form_bank.add_error(None, ('El pago mensual es insuficiente, ya que es igual o menor '
                                              'al interés generado. Esto provocaría una deuda interminable. '
                                              'Intenta con un pago mensual mayor al interés del préstamo '
                                              'para que se pueda finalizar el pago.'))

                    return render(request, self.template_name, context)

                new_loan = no_bank_desc_loan(payment, loan_interest, loan_amount)
                result = json.dumps(new_loan)

                no_bank = form_bank.save(commit=False)
                no_bank.name = name
                no_bank.interest_rate = loan_interest
                no_bank.loan_amount = result
                no_bank.save()

                return redirect(reverse_lazy('loan:no_bank_detail', args=[pk]))

            else:
                return render(request, self.template_name, context)


        elif "calculator-submit" in request.POST:
            if form.is_valid():
                loan_amount = float(form.cleaned_data['loan_amount'])
                month_pay = float(form.cleaned_data['month_pay'])
                loan_interest = float(form.cleaned_data['loan_interest'])

                if loan_amount * (
                        loan_interest / 100) >= month_pay:  # This is to avoid infinite loan, the interest*loan amount is more that the mon pay it will never ends
                    # and this could kill the server.
                    form.add_error(None, ('El pago mensual es insuficiente, ya que es igual o menor '
                                          'al interés generado. Esto provocaría una deuda interminable. '
                                          'Intenta con un pago mensual mayor al interés del préstamo para que se pueda '
                                          'finalizar el pago.'))  # Displaying error message if pre applied

                    return render(request, self.template_name, context)

                else:
                    data = Loans(loan_amount, month_pay, loan_interest)
                    result = data.pay_loan_amount()  # This should be a list of dicts
                    request.session['result'] = json.dumps(result)
                    return redirect(reverse_lazy('loan:no_bank_detail', args=[pk]))


            return render(request, self.template_name, context)

        return render(request, self.template_name, context)


class BankGeristerCreateView(LoginRequiredMixin, CreateView):
    model = BankLoan
    success_url = "loan:nobank_list.html"
    template_name = "loan/bank_loan.html"
    form_class = BankLoanForm

    def form_valid(self, form):

        bank = form.save(commit=False)
        bank.user = self.request.user
        bank.save()
        return super().form_valid(form)

























