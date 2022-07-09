from django.urls import path
from .views import profile, LoginView, refresh_token, register


urlpatterns = [
    path('profile', profile, name='profile'),
    path('login', LoginView.as_view(), name='login'),
    path('refresh-token/', refresh_token, name='refresh_token'),
    path('register', register, name='register'),
]