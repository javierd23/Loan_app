from django.db import models

class Loan(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    loan_amount = models.FloatField()
    monthly_interest = models.FloatField()
    monthly_payment = models.FloatField()

    def __str__(self):
        return self.name






