from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):
    return HttpResponse("Hello, world. You are seening the first app t"
                        "hat will calculte your loan for you.")


