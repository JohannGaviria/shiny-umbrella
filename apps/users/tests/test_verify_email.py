from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.users.models import VerifyAccount
from apps.users.utils import generate_verification_token


# Tests para la verificación de correo electrónico
class VerifyEmailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='TestUsername',
            email='test@email.com'
        )
        self.user.set_password('TestPassword')
        self.user.save()
        self.verify_account = VerifyAccount.objects.create(user=self.user)
        self.token = generate_verification_token(self.user.email)
        self.url = reverse('verify_email', args=[self.token])


    # Prueba de verificación de email exitoso
    def test_verify_email_successful(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    # Prueba de verificación con token inválido
    def test_verify_email_invalid_token(self):
        self.url = reverse('verify_email', args=['invalid_token_string'])
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    # Prueba de verificación cuando el email ya ha sido verificado
    def test_verify_email_already_verified(self):
        self.verify_account.email_verified = True
        self.verify_account.save()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    # Prueba de verificación para un usuario que no existe
    def test_verify_email_user_not_found(self):
        self.user.delete()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    # Prueba de verificación para una cuenta de verificación que no existe
    def test_verify_email_verification_account_not_found(self):
        self.verify_account.delete()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
