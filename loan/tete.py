# let's build a program that tells you how much you pay for a loan for an entire time.
import math


class Loans:

    def __init__(self, loan, pays, rate):
        self.loan_amount = loan
        self.monthly_payment = pays
        self.loan_interest = rate
        self.interest_rate = rate / 100

    def pay_loan_amount(self):
        total = []
        monthly_pays = 0
        last_pay = 0
        remaining = 0
        total_interest = 0
        months = 0
        while True:
            desc_pay = self.monthly_payment - (self.loan_amount * self.interest_rate)
            discount_loan = self.loan_amount - desc_pay
            self.loan_amount = discount_loan                        #This will get the remaining of the loan each time.
            monthly_pays = self.monthly_payment + monthly_pays
            interest_pay = (self.loan_amount * self.interest_rate)
            total_interest += interest_pay
            desc_int = self.monthly_payment - desc_pay
            months = months + 1
            total.append(
                {"month": months,
                 "monthly_pay": round(self.monthly_payment),
                 "des_pay": round(desc_pay),
                 "des_int": round(desc_int),
                 "loan_amount": round(self.loan_amount)}
                            )
            if self.loan_amount < 0: break

        return {
        "schedule": total, #this is the whole dict and the following is just to get some info in the a different display
        "month_pay": round(self.monthly_payment, 2),
        "desc_pay": round(desc_pay, 2),
        "des_int": round(desc_int, 2),  # Back to %
        "loan_amount": round(self.loan_amount, 2)
    }


#loan1 = Loans(150000, 39800, 10)

#print(loan1.pay_loan_amount())


#In this program we will call culculate the quote for a bank loan.

class Bank:
    def __init__(self, loan, rate, months):
        self.loan_amount = loan
        self.months = months
        self.loan_interest = rate
        self.interest_rate = rate / 100


    def bank_loan(self):
        loan_amount = self.loan_amount
        interest_rat = self.interest_rate / 12
        rate_int = interest_rat * (1 + interest_rat)**self.months
        rate_down = (1 + interest_rat)**self.months - 1
        month_pay = self.loan_amount  * rate_int / rate_down

        total = []
        months_count = 0
        while True:
            dec_pay = month_pay - (self.loan_amount  * interest_rat)
            desc_amount = self.loan_amount - dec_pay
            self.loan_amount = desc_amount
            desc_pay = interest_rat * self.loan_amount
            pay_month = month_pay - desc_pay
            months_count +=  1

            total.append(
                {"month": months_count,
                 "monthly_payment": round(month_pay, 2),
                 "principal": round(pay_month, 2),
                 "interest": round(desc_pay, 2),
                 "remaining_balance": round(max(self.loan_amount, 0), 2)}
                )

            if self.loan_amount  <= 0: break
        return {
        "schedule": total, #this is the whole dict and the following is just to get some info in the a different display
        "month_pay": round(month_pay, 2),
        "loan_amount_total": round(loan_amount, 2),
        "interest_rate": round(self.loan_interest, 2),  # Back to %
        "months": self.months
    }

#result = Bank(100000,5, 40)
#print(result.bank_loan())


def no_bank_desc_loan(payment, interest_rate, loan_amount):

    desc_loan = (interest_rate / 100) * loan_amount

    loan_desc = payment - desc_loan
    new_loan_amount = round(loan_amount - loan_desc)

    return new_loan_amount
#Testing function...
#print(no_bank_desc_loan(1000,5, 15000))


#This class will get the payments for a bank loan,
# instead of calculating the monthly payment, it will take it as input.

class BankLoanUser:
    def __init__(self,monthly_payment, loan, rate, months):
        self.monthly_payment = monthly_payment
        self.loan_amount = loan
        self.months = months
        self.loan_interest = rate
        self.interest_rate = rate / 100

    def bank_loan(self):
        loan_amount = self.loan_amount
        interest_rat = self.interest_rate / 12
        rate_int = interest_rat * (1 + interest_rat) ** self.months
        rate_down = (1 + interest_rat) ** self.months - 1
        month_pay = self.loan_amount * rate_int / rate_down

        if month_pay != self.monthly_payment:
            month_pay = self.monthly_payment

        total = []
        months_count = 0
        while True:
            dec_pay = month_pay - (self.loan_amount * interest_rat)
            desc_amount = self.loan_amount - dec_pay
            self.loan_amount = desc_amount
            desc_pay = interest_rat * self.loan_amount
            pay_month = month_pay - desc_pay
            months_count += 1

            total.append(
            {"month": months_count,
             "monthly_payment": round(month_pay, 2),
             "principal": round(pay_month, 2),
             "interest": round(desc_pay, 2),
             "remaining_balance": round(max(self.loan_amount, 0), 2)}
                    )

            if self.loan_amount <= 0: break
        return total

#testing BankLoanUser class...
loan_1 = BankLoanUser(1300,15000,5, 12)
result = loan_1.bank_loan()


data = [ item for item in result ]











