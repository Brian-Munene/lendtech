from django.urls import path
from .views import profile, login
urlpatterns = [
    path('profile', profile, name='profile'),
    path('login', login, name='login')
]