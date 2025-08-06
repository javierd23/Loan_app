from django.db import models

from django.contrib.auth.models import User


class NoBankLoan(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_payment = models.DecimalField(verbose_name="Pagos mensuales",
                                          max_digits=10, decimal_places=2, null=True, blank=True)
    loan_amount = models.DecimalField(verbose_name="Monto del préstamo",
                                      max_digits=10, decimal_places=2 )
    interest_rate = models.DecimalField(verbose_name="Intereses mensuales",
                                        max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
















