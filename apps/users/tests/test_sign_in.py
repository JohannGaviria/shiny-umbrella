from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# Tests para el inicio de sesión de usuario
class SignInTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('sign_in')
        self.user = User.objects.create(
            username='TestUsername',
            email='test@email.com'
        )
        self.user.set_password('TestPassword')
        self.user.save()
        self.data = {
            'email': 'test@email.com',
            'password': 'TestPassword'
        }


    def test_sign_in_user_successful(self):
        """
        Prueba de inicio de sesión de usuario exitoso.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    def test_sign_in_user_with_invalid_email(self):
        """
        Prueba de inicio de sesión de usuario con email inválido.
        """
        self.data['email'] = 'incorrect@email.com'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)

    
    def test_sign_in_user_with_invalid_password(self):
        """
        Prueba de inicio de sesión de usuario con contraseña inválida.
        """
        self.data['password'] = 'incorrectPassword'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_sign_in_user_inactive(self):
        """
        Prueba de inicio de sesión para usuario inactivo.
        """
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)