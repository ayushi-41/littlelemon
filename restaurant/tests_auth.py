from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class AuthTests(APITestCase):

    def test_user_registration(self):
        """
        Ensure we can create a new user via registration endpoint
        """
        url = '/auth/users/'  # Djoser registration endpoint
        data = {
            "username": "testuser",
            "password": "testpassword123",
            "email": "testuser@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_user_login(self):
        """
        Ensure a registered user can obtain a token
        """
        # First, create a user
        user = User.objects.create_user(username="loginuser", password="loginpass123")
        
        # Attempt login using Djoser token endpoint
        url = '/auth/token/login/'  # Djoser token endpoint
        data = {
            "username": "loginuser",
            "password": "loginpass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)
