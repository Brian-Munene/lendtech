from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BankAccountTransactions, Payments, Loans
from accounts.models import BankAccounts

User = get_user_model()


@receiver(post_save, sender=Payments)
def update_balance_after_payment(sender, instance, created, **kwargs):
    if created:
        payer = BankAccounts.objects.get(pk=instance.payer.id)
        payee = BankAccounts.objects.get(pk=instance.payee.id)

        payer.amount = float(payer.amount) - float(instance.amount)
        payer.save()

        payee.amount = float(payee.amount) + float(instance.amount)
        payee.save()

        BankAccountTransactions.objects.create(
            account_from=payer,
            account_to=payee,
            amount=instance.amount,
            transaction_type='PAYMENT'
        )


@receiver(post_save, sender=Loans)
def update_balance_after_receiving_loan(sender, instance, created, **kwargs):
    if created:
        borrower = BankAccounts.objects.get(pk=instance.borrower.id)
        borrower.amount = float(borrower.amount) + float(instance.amount)
        borrower.save()
        BankAccountTransactions.objects.create(
            account_from=BankAccounts.objects.exclude(id=borrower.id).first(),
            account_to=borrower,
            amount=instance.amount,
            transaction_type='LOAN'
        )
