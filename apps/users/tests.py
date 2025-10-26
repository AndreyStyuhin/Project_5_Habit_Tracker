from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User


class UserAuthTests(APITestCase):

    def test_user_registration(self):
        """Тест успешной регистрации пользователя."""
        url = reverse('users:user_register')
        data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            "telegram_id": "98765"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "testuser@example.com")
        self.assertTrue(User.objects.get().check_password("testpassword123"))

    def test_user_login(self):
        """Тест получения JWT токена (логин)."""
        # Сначала регистрируем пользователя
        user = User.objects.create_user(
            email="login@example.com",
            password="loginpass123"
        )

        url = reverse('token_obtain_pair')
        data = {
            "email": "login@example.com",
            "password": "loginpass123"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_fail(self):
        """Тест неудачного логина."""
        url = reverse('token_obtain_pair')
        data = {
            "email": "wrong@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)