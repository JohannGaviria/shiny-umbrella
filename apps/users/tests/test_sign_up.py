from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# Tests para el registro de usuario
class SignUpTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('sign_up')
        User.objects.create(
            username='TestExistingUsername',
            email='testexisting@email.com',
            password='TestPassword'
        )
        self.data = {
            'username': 'TestUsername',
            'email': 'test@email.com',
            'password': 'TestPassword',
        }


    def test_sign_up_user_successful(self):
        """
        Prueba de registro de usuario exitoso.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    def test_sign_up_user_invalid_data(self):
        """
        Prueba de registro de usuario con datos inválidos.
        """
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_sign_up_user_existing_username(self):
        """
        Prueba de registro de usuario con nombre de usuario existente.
        """
        self.data['username'] = 'TestExistingUsername'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_sign_up_user_existing_email(self):
        """
        Prueba de registro de usuario con correo electrónico existente.
        """
        self.data['email'] = 'testexisting@email.com'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)

    
    def test_sign_up_user_whit_weak_password(self):
        """
        Prueba de registro de usuario con contraseña debil.
        """
        self.data['password'] = '123'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)
