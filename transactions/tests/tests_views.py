from rest_framework.test import APITestCase, force_authenticate
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()

from ..models import Loans, Payments, BankAccountTransactions

class TestLoans(APITestCase):

    def authenticate(self):
        # self.client.post(reverse('register'),{
        #     "username": "Ian",
        #     "email": "Ian@gmail.com",
        #     "first_name": "Ian",
        #     "last_name": "Nene",
        #     "password": "secretkey",
        #     "confirm_password": "secretkey",
        #     "phone_number": "0706484207",
        #     "user_type": "INDIVIDUAL",
        #     "number": "12343",
        #     "account_type": "BANK"
        # })
        # response = self.client.post(reverse("login"),{
        #     "username": "Ian@gmail.com",
        #     "password": "secretkey"
        # })
        # self.client.credentials(HTTP_AUTHORIZATION=f"Token  {response.data['token']}")
        # force_authenticate(response, user=self.user)
        user = User.objects.create(
            username="Brian",
            email="Brian@gmail.com",
            first_name="Brian",
            last_name="Munene",
            password="secretkey",
            phone_number="0706484701",
            user_type="INDIVIDUAL",
        )
        client = APIClient()
        client.force_authenticate(user=user)

    def test_should_not_view_loans_with_no_auth(self):
        response = self.client.get(reverse("loans-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_view_loans(self):
        self.authenticate()
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
        ian = User.objects.create(
            username="ian",
            email="ian@gmail.com",
            first_name="Brian",
            last_name="Munene",
            password="secretkey",
            phone_number="0706484711",
            user_type="INDIVIDUAL",
        )
        self.casper = Payments.objects.create(
                payer=brian.id,
                payee=ian.id,
                amount=1000.00
            )
        self.muffin = Payments.objects.create(
                payer=brian.id,
                payee=ian.id,
                amount=1000.00
            )
        self.rambo = Payments.objects.create(
                payer=brian.id,
                payee=ian.id,
                amount=1000.00
            )
        self.ricky = Payments.objects.create(
                payer=brian.id,
                payee=ian.id,
                amount=1000.00
            )

    def authenticate(self):
        user = User.objects.create(
            username="Brian",
            email="Brian@gmail.com",
            first_name="Brian",
            last_name="Munene",
            password="secretkey",
            phone_number="0706484701",
            user_type="INDIVIDUAL",
        )
        client = APIClient()
        client.force_authenticate(user=user)

    def test_should_not_view_payments_with_no_auth(self):
        response = self.client.get(reverse("payments-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_view_payment(self):
        self.authenticate()
        response = self.client.get(reverse("payments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
