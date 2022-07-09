from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'is_active']



class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User

        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'password', 'confirm_password', 'user_type']
        
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
        # Use the `create_user` method we wrote earlier to create a new user.
        # return User.objects.create_user(**validated_data)
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
        return user