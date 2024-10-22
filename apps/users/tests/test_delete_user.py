from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# Tests para la eliminación de usuario
class DeleteUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('delete_user')
        self.user = User.objects.create(
            username='TestUsername',
            email='test@email.com'
        )
        self.user.set_password('TestPassword')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)


    def test_delete_user_successful(self):
        """
        Prueba de eliminación de usuario exitosa.
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_delete_user_without_token(self):
        """
        Prueba de eliminación de usuario sin token.
        """
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
