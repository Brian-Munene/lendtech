from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import User, BankAccounts


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = ['id', 'name', 'number', 'account_type', 'user', 'amount', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    bank_account = serializers.SerializerMethodField()

    def get_bank_account(self, obj):
        return BankAccountSerializer(BankAccounts.objects.get(user=obj)).data

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'is_active', 'bank_account']


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    number = serializers.CharField(required=True)
    account_type = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'password', 'confirm_password',
                  'number', 'account_type', 'user_type']
        
        extra_kwargs = {
            "email":      {"required": True},
            'username': {'required': True},
            'phone_number':  {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields did not match."})

        if User.objects.filter(email__exact=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already in use."})
        
        if User.objects.filter(username__exact=attrs['username']).exists():
            raise serializers.ValidationError({"user": "Username already in use."})

        attrs['phone_number'] = self.validate_phone(attrs['phone_number'])

        if User.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "Phone Number already in user."})

        return attrs
    
    def validate_phone(self, phone):
        import re
        phone_number = phone
        phone = phone_number.strip("+")
        phone = phone if phone[:3] != '254' else phone.replace('254', '', 1)
        phone = re.sub('[^0-9]+', '', phone)
        phone = phone if phone[0] != '0' else phone.replace('0', '', 1)
        code = 254
        clean_phone = f'{code}{phone}'
        return clean_phone

    def create(self):
        user = User.objects.create(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
            user_type=self.validated_data['user_type'],
        )
        user.set_password(self.validated_data['password'])
        user.save()

        bank_account = BankAccounts.objects.create(
            name=self.validated_data['username'],
            number=self.validated_data['number'],
            account_type=self.validated_data['account_type'],
            user=user
        )
        bank_account.save()
        return user

#
# class CreateBankAccountSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = BankAccounts
#         fields = ['name', 'number', 'account_type', 'user', 'amount']
#
#     extra_kwargs = {
#         "name": {"required": True},
#         'number': {'required': True},
#         'account_type': {'required': True},
#         'amount': {'required': True}
#     }
#
#     def validate(self, attrs):
#         if not User.objects.filter(email__exact=attrs['user']).exists():
#             raise serializers.ValidationError({"user": "Pleas enter a valid user"})
#
#         if attrs['amount'] < 0:
#             raise serializers.ValidationError({"amount": "Amount is invalid"})
#
#         return attrs
#
#     def create(self):
#         bank_account = BankAccounts.objects.create(
#             name=self.validated_data['name'],
#             number=self.validated_data['number'],
#             account_type=self.validated_data['account_type'],
#             user=self.validated_data['user'],
#             amount=self.validated_data['amount'],
#         )
#         bank_account.save()
#
#         return bank_account
