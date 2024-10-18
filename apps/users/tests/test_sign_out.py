from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Tests para el cierre de sesión
class SignOutTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('sign_out')
        self.user = User.objects.create(
            username='TestUsername',
            email='test@email.com'
        )
        self.user.set_password('TestPassword')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    # Prueba de cierre de sesión de usuario exitoso
    def test_sign_out_user_successful(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)

    # Prueba de cierre de sesión de usuario sin token
    def test_sign_out_user_without_token(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
