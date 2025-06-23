import json
from django.contrib import messages
from http.client import responses
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .tete import Bank

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
            messages.error(request, "Invalid input provided.")
            return redirect(request.path)

        data = Bank(loan_amount, loan_rate, loan_months)
        result = data.bank_loan()  # This should be a list of dicts
        request.session['result'] = json.dumps(result)
        return redirect(request.path)








def no_bank(request):
    return render(request, "loan/no_bank.html")



