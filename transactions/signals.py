from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BakAccountTransactions, Payments, Loans
from accounts.models import BankAccounts

User = get_user_model()


@receiver(post_save, sender=Payments)
def update_balance_after_payment(sender, instance, created, **kwargs):
    if created:
        payer = BankAccounts.objects.get(pk=instance.payer)
        payee = BankAccounts.objects.get(pk=instance.payee)

        payer.amount = float(payer.amount) - float(instance.amount)
        payee.amount = float(payee.amount) + float(instance.amount)


@receiver(post_save, sender=Loans)
def update_balance_after_receiving_loan(sender, instance, created, **kwargs):
    if created:
        borrower = BankAccounts.objects.get(pk=instance.borrower)
        borrower.amount = float(borrower.amount) + float(instance.amount)
