from rest_framework import serializers
from .models import Loans, Payments, BankAccountTransactions


class LoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = ['borrower', 'amount']


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['payer', 'payee', 'amount']


class BankAccountTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountTransactions
        fields = ['account_from', 'account_to', 'amount', 'transaction_type']
