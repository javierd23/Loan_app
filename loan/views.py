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
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from .models import NoBankLoan, BankLoan, BankLoanDetail

from .forms import LoanPaymentForm, BankForm, NobanForm, BankLoanForm
from .tete import Bank, Loans, no_bank_desc_loan, BankLoanUser

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
                form.add_error(None, 'No mas de 600 meses y menos de 1 mes es permitido.')  # Displaying error message...
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



#register your loans view.
class RegisterLoanView(LoginRequiredMixin, View):
    """A simple view to select the type of loan."""

    def get(self, request):
        return render(request, 'loan/register_loan.html')



class NoBankCreateView(LoginRequiredMixin, CreateView):
    template_name = "loan/nobank_loan.html"
    form_class = NobanForm
    model = NoBankLoan
    success_url = "loan/bank_list.html"

    def form_valid(self, form):

        no_bank = form.save(commit=False)
        no_bank.user = self.request.user
        no_bank.save()
        return super().form_valid(form)


class BankListView(LoginRequiredMixin, ListView):
    template_name = "loan/banks_list.html"
    context_object_name = 'no_bank_loans'

    def get_queryset(self, **kwargs):
        return NoBankLoan.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bank_loans"] = BankLoan.objects.filter(user=self.request.user)
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


class NoBankLoanDeleteView(LoginRequiredMixin, DeleteView):
    model = NoBankLoan
    context_object_name = 'no_bank'
    template_name = 'loan/no_bank_delete.html'
    success_url = reverse_lazy('loan:bank_list')


class BankCreateView(LoginRequiredMixin, View):
    """This view will create the Bank loan and its payments
        that it will be then displayed in the detail view."""
    template_name = "loan/bank_loan.html"

    def get(self, request):

        form_loan = BankLoanForm(prefix='loan')
        form = BankForm(prefix='calculator')
        result_json = request.session.pop('result', None)

        try:
            result = json.loads(result_json) if result_json else None
        except json.JSONDecodeError:
            result = None
            messages.error(request, "Error al leer los resultados anteriores.")

        context = {"form_loan": form_loan, "form": form, "result": result}

        return render(request, self.template_name, context)


    def post(self, request):
        form_loan = BankLoanForm(request.POST, prefix='loan')
        form = BankForm(request.POST, prefix='calculator')

        context = {"form_loan": form_loan, "form": form}

        if "calculator-submit" in request.POST:

            if form.is_valid():
                loan_amount = float(form.cleaned_data['loan_amount'])
                int_rate = int(form.cleaned_data['int_rate'])
                months =  int(form.cleaned_data['months'])

                if months < 1 or months > 600:
                    form_loan.add_error(None, (
                        'No mas de 600 meses y menos de 1 mes es permitido.'))  # Displaying error message...
                    return render(request, self.template_name, context)

                data = Bank(loan_amount, int_rate, months)
                result = data.bank_loan()  # This should be a list of dicts
                request.session['result'] = json.dumps(result)
                return redirect(request.path)

            return render(request, self.template_name, context)

        elif "loan-submit" in request.POST:

            if form_loan.is_valid(): #Grabbing the data to create the detail of the payment.
                monthly_payment = float(form_loan.cleaned_data['monthly_payment'])
                interest_rate = int(form_loan.cleaned_data['interest_rate'])
                loan_amount = float(form_loan.cleaned_data['loan_amount'])
                months = int(form_loan.cleaned_data['months'])
                month_paid = int(form_loan.cleaned_data['month_paid'])

                if months < 1 or months > 600: #No more than 600 months, to avoid issues with the server.
                    form.add_error(None, "No mas de 600 meses y menos de 1 mes es permitido.")
                    return render(request, self.template_name, context)

                loan_bank = form_loan.save(commit=False)
                loan_bank.user = self.request.user
                loan_bank.save()

                loan = BankLoanUser(monthly_payment, loan_amount, interest_rate, months)
                loan_result = loan.bank_loan() #This is a list of dicts...


                # if the user's loan has been paid form months, I get the data from that month and on...
                if month_paid == 0:
                    loan_data = loan_result[:]  # if there is no month paid yet, I get all the data.
                else:
                    loan_data = loan_result[month_paid:]

                BankLoanDetail.objects.bulk_create(
                    [
                        BankLoanDetail(
                            months=json.dumps(item["month"]),
                            payment=json.dumps(item["monthly_payment"]),
                            principal=json.dumps(item["principal"]),
                            interest_rate=json.dumps(item["interest"]),
                            remaining=json.dumps(item["remaining_balance"]),
                            bankloan = loan_bank
                                        )
                            for item in loan_data

                    ]

                )

                return redirect(reverse_lazy('loan:bank_list'))

        return render(request, self.template_name, context)


class BankLoanDetailView(LoginRequiredMixin, DetailView):
    model = BankLoan
    template_name = "loan/bank_detail.html"
    context_object_name = "bank_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["loan_details"] = BankLoanDetail.objects.filter(bankloan=self.object)
        return context


class BankLoanDeleteView(LoginRequiredMixin, DeleteView):
    model = BankLoan
    template_name = "loan/bank_delete.html"
    context_object_name = "bank_loan"
    success_url = reverse_lazy('loan:bank_list')






















