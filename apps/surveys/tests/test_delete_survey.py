from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from apps.surveys.models import Survey
from faker import Faker
from datetime import timedelta
import random


fake = Faker()


# Tests para eliminar encuesta
class DeleteSurveyTestsCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='TestUsername',
            email='test@email.com',
        )
        self.user.set_password('TestPassword')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.user_not_create = User.objects.create(
            username=fake.user_name(),
            email=fake.email(),
        )
        self.user.set_password(fake.password())
        self.user.save()
        self.survey = Survey.objects.create(
            title=fake.sentence(nb_words=6),
            description=fake.text(max_nb_chars=200),
            end_date=timezone.now() + timedelta(days=random.randint(1, 30)),
            is_public=True,
            user=self.user
        )
        self.url = reverse('delete_survey', args=[self.survey.id])

    
    def test_delete_survey_successfully(self):
        """
        Prueba de eliminar una encuesta exitosamente.
        """
        response = self.client.delete(self.url, format='josn')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_delete_survey_not_found(self):
        """
        Prueba de eliminar encuesta que no existe
        """
        url = reverse('delete_survey', args=['ec7f051a960d42788a10ff51cc85dc23'])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
    

    def test_delete_survey_user_is_not_create(self):
        """
        Prueba de eliminar encuesta que el usuario no es el creador.
        """
        self.client.force_authenticate(user=self.user_not_create)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
    

    def test_delete_survey_without_token(self):
        """
        Prueba de eliminar encuesta sin token.
        """
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
