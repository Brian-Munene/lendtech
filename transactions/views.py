from rest_framework import viewsets
from django_filters import rest_framework as filters, DateFilter
from .models import Payments, Loans, BankAccountTransactions
from .serializers import PaymentsSerializer, LoansSerializer, BankAccountTransactionSerializer


class PaymentsViewset(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class LoansFilter(filters.FilterSet):
    start_date = DateFilter(field_name='created_at', lookup_expr='gt')
    end_date = DateFilter(field_name='created_at', lookup_expr='lt')


    class Meta:
        model = Loans
        fields = ['created_at']


class LoansViewset(viewsets.ModelViewSet):
    queryset = Loans.objects.all()
    serializer_class = LoansSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LoansFilter


class BankAccountTransactionsViewsets(viewsets.ModelViewSet):
    queryset = BankAccountTransactions.objects.all()
    serializer_class = BankAccountTransactionSerializer

