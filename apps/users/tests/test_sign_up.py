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


    # Prueba de registro de usuario exitoso
    def test_sign_up_user_successful(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    # Prueba de registro de usuario con datos inválidos
    def test_sign_up_user_invalid_data(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    # Prueba de registro de usuario con nombre de usuario existente
    def test_sign_up_user_existing_username(self):
        self.data['username'] = 'TestExistingUsername'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    # Prueba de registro de usuario con correo electrónico existente
    def test_sign_up_user_existing_email(self):
        self.data['email'] = 'testexisting@email.com'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)

    
    # Prueba de registro de usuario con contraseña poco segura
    def test_sign_up_user_password_no_secure(self):
        self.data['password'] = '123'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)
