from django.urls import path
from .views import profile, login, refresh_token, register


urlpatterns = [
    path('profile', profile, name='profile'),
    path('login', login, name='login'),
    path('refresh-token/', refresh_token, name='refresh_token'),
    path('register', register, name='register'),
]