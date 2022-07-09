import uuid
from django.db import models
from accounts.models import BankAccounts
from django.contrib.auth import get_user_model
User = get_user_model()


TRANSACTION_TYPES = (
    ('LOAN', 'LOAN'),
    ('PAYMENT', 'PAYMENT')
    )


class Loans(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    borrower = models.ForeignKey(BankAccounts, on_delete=models.SET_NULL, related_name='borrower',
                                 related_query_name='borrower', blank=False, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payments(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    payer = models.ForeignKey(BankAccounts, on_delete=models.SET_NULL, related_name='payer', related_query_name='payer',
                              blank=False, null=True)
    payee = models.ForeignKey(BankAccounts, on_delete=models.SET_NULL, related_name="payee", related_query_name='payee',
                              blank=False, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BankAccountTransactions(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    account_from = models.ForeignKey(BankAccounts, on_delete=models.SET_NULL, related_name="account_from",
                                     related_query_name='account_from', blank=False, null=True)
    account_to = models.ForeignKey(BankAccounts, on_delete=models.SET_NULL, related_name="account_to",
                                   related_query_name='account_to', blank=False, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES, default='INDIVIDUAL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
