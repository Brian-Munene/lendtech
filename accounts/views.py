from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.views import APIView
from .utils import get_tokens_for_user
import jwt
from django.conf import settings

from django.views.decorators.csrf import csrf_protect
from .serializers import UserSerializer, RegistrationSerializer, BankAccountSerializer


User = get_user_model()


@api_view(['GET'])
def profile(request):
    user = request.user
    serialized_user = UserSerializer(user).data
    return Response({'user': serialized_user})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    user_serializer = RegistrationSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.create()

        response = Response()
        _user = User.objects.filter(phone_number=user_serializer.data['phone_number']).first()

        response.data = {
            'user': UserSerializer(_user).data,
        }
        return response
    else:
        data = user_serializer.errors
        return Response(data)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        User = get_user_model()
        email = request.data.get("username")
        password = request.data.get("password")
        response = Response()
        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed("email and password required")
        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed("user not found")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("wrong password")

        token = get_tokens_for_user(user)
        response.data = token
        return response


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def refresh_token(request):
    '''
    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    '''
    User = get_user_model()
    refresh_token = request.COOKIES.get('refreshtoken')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            'expired refresh token, please login again.')

    user = User.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')

    access_token = generate_access_token(user)
    return Response({'access_token': access_token})

