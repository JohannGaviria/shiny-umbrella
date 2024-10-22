from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# Tests para la actualización de usuario
class UpdateUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('update_user')
        self.user = User.objects.create(
            username='TestUsername',
            email='test@email.com'
        )
        self.user.set_password('TestPassword')
        self.user.save()
        User.objects.create(
            username='TestExistingUsername',
            email='testexisting@email.com',
            password='TestPassword'
        )
        self.data = {
            'username': 'TestNewUsername',
            'email': 'testnew@email.com',
            'current_password': 'TestPassword',
            'new_password': 'TestNewPassword'
        }
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)


    def test_update_user_successful(self):
        """
        Prueba de actualización de usuario exitoso.
        """
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    def test_update_user_invalid_data(self):
        """
        Prueba de actualización de usuario con datos inválidos.
        """
        self.data['username'] = ''
        self.data['email'] = ''
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_update_user_existing_username(self):
        """
        Prueba de actualización de usuario con nombre de usuario existente.
        """
        self.data['username'] = 'TestExistingUsername'
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_update_user_existing_email(self):
        """
        Prueba de actualización de usuario con correo electrónico existente.
        """
        self.data['email'] = 'testexisting@email.com'
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)

    
    def test_update_user_whit_weak_password(self):
        """
        Prueba de actualización de usuario con contraseña debil.
        """
        self.data['new_password'] = '123'
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_update_user_without_token(self):
        """
        Prueba de actualización de usuario sin token.
        """
        self.client.force_authenticate(user=None)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
