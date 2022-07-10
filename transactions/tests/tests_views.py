from rest_framework.test import APITestCase, force_authenticate
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()

from ..models import Loans, Payments, BankAccountTransactions
from accounts.models import BankAccounts


class TestLoans(APITestCase):

    def setUp(self):
        user = User.objects.create(
            username="Brian",
            email="Brian@gmail.com",
            first_name="Brian",
            last_name="Munene",
            password="secretkey",
            phone_number="0706484701",
            user_type="INDIVIDUAL",
        )
        self.client.force_authenticate(user=user)

    def test_should_not_view_loans_with_no_auth(self):
        client = APIClient()
        response = client.get(reverse("loans-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_view_loans(self):
        response = self.client.get(reverse("loans-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPayments(APITestCase):

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
        self.casper = Payments.objects.create(
                payer=brian_account,
                payee=ian_account,
                amount=1000.00
            )

        user = User.objects.create(
            username="Ryan",
            email="Ryan@gmail.com",
            first_name="Ryan",
            last_name="Munene",
            password="secretkey",
            phone_number="0706484721",
            user_type="INDIVIDUAL",
        )
        self.client.force_authenticate(user=user)

    def test_should_not_view_payments_with_no_auth(self):
        client = APIClient()
        response = client.get(reverse("payments-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_view_payment(self):
        response = self.client.get(reverse("payments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
