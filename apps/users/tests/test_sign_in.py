from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# Tests para el inicio de sesión
class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('sign_in')
        user = User.objects.create(
            username='TestUsername',
            email='test@email.com'
        )
        user.set_password('TestPassword')
        user.save()
        self.data = {
            'username': 'TestUsername',
            'password': 'TestPassword'
        }


    # Prueba de inicio de sesión de usuario exitoso
    def test_sign_in_user_successful(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    # Prueba de inicio de sesión de usuario inválido
    def test_sign_in_user_invalid_email(self):
        self.data['username'] = 'incorrectUsername'
        self.data['password'] = 'incorrectPassword'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)
