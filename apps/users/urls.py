from django.urls import path
from .views import UserCreateAPIView

app_name = 'users'

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
]
