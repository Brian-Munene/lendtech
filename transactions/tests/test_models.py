from django.test import TestCase
from transactions.models import Loans, Payments
from accounts.models import BankAccounts
from django.contrib.auth import get_user_model
User = get_user_model()


class TestPayments(TestCase):

    def setUp(self):
        brian = User.objects.create(
            username="Brian",
            email="Brian@gmail.com",
            first_name="Brian",
            last_name="Munene",
            password="secretkey",
            phone_number="0706484701",
            user_type="INDIVIDUAL",
        )
        brian_account = BankAccounts.objects.create(
            user_id=brian.id,
            name=brian.username,
            number=brian.phone_number,
            account_type='MOBILE'
        )
        ian = User.objects.create(
            username="ian",
            email="ian@gmail.com",
            first_name="Brian",
            last_name="Munene",
            password="secretkey",
            phone_number="0706484711",
            user_type="INDIVIDUAL",
        )
        ian_account = BankAccounts.objects.create(
            user_id=ian.id,
            name=ian.username,
            number=ian.phone_number,
            account_type='MOBILE'
        )
        self.payment = Payments.objects.create(
                payer=brian_account,
                payee=ian_account,
                amount=1000.00
            )
        self.loans = Loans.objects.create(
            borrower=ian_account,
            amount=20000.00
        )

    def test_payment_amount_is_saved(self):
        self.assertEqual(self.payment.amount, float(1000))

    def test_loan_amount_is_saved(self):
        self.assertEqual(self.loans.amount, float(20000))
