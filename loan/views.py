from http.client import responses
from django.http import HttpResponse
from django.shortcuts import render, redirect

def bank(request):
    return render(request, "loan/bank.html")


def no_bank(request):
    return render(request, "loan/no_bank.html")



