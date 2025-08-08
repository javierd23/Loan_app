import datetime
from django.utils import timezone

from django.db import models

from django.contrib.auth.models import User


class NoBankLoan(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_payment = models.DecimalField(verbose_name="Pagos mensuales",
                                          max_digits=10, decimal_places=2, null=True, blank=True)
    interest_rate = models.IntegerField(verbose_name="Intereses mensuales")
    loan_amount = models.DecimalField(verbose_name="Monto del préstamo",
                                      max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BankLoan(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_payment = models.DecimalField(verbose_name="Pagos mensuales",
                                          max_digits=10, decimal_places=2)
    interest_rate = models.IntegerField(verbose_name="Intereses Anual")
    loan_amount = models.DecimalField(verbose_name="Monto del préstamo",
                                      max_digits=10, decimal_places=2)
    month_paid = models.IntegerField(verbose_name="Meses pagados" , default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name










