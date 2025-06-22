import json
from http.client import responses
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .tete import Bank

class BankView(View):
    def get(self, request):
        result = request.session.get('result', False)
        if result:
            del request.session['result']

        return render(request, "loan/bank.html", {'result': result})

    def post(self, request):
        loan_amount = float(request.POST.get('loan_amount'))
        loan_rate = float(request.POST.get('loan_rate'))
        loan_months = float(request.POST.get('loan_months'))

        data = Bank(loan_amount, loan_rate, loan_months)
        result = data.bank_loan()
        result = {"result": result}
        request.session['result'] = result
        return redirect(request.path)








def no_bank(request):
    return render(request, "loan/no_bank.html")



