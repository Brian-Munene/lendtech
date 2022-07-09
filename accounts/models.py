from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

USER_TYPES = (
    ('INDIVIDUAL', 'INDIVIDUAL'),
    ('CORPORATE', 'CORPORATE')
    )

BANK_ACCOUNT_TYPES = (
    ('BANK', 'BANK'),
    ('MOBILE', 'MOBILE')
)


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_type = models.CharField(max_length=30, choices=USER_TYPES, default='INDIVIDUAL')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "phone_number",
        "username"
    ]


class BankAccounts(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    number = models.CharField(max_length=255, unique=True)
    account_type = models.CharField(max_length=20, choices=BANK_ACCOUNT_TYPES, default='BANK')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
