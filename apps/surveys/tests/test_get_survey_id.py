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


# Tests para la obtener una encuesta por su ID
class GetSurveyIdTestsCase(TestCase):
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
        self.url = reverse('get_survey_id', args=[self.survey.id])

    
    def test_get_survey_id_successful(self):
        """
        Prueba de obtener una encuesta con su id exitosamente.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    def test_get_survey_id_not_found(self):
        """
        Prueba de obtener una encuesta con su id que no se encuentra.
        """
        url = reverse('get_survey_id', args=['ec7f051a960d42788a10ff51cc85dc23'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_get_survey_id_is_private_user_is_create(self):
        """
        Prueba de obtener una encuesta con su id que es privada y el usuario es su creador.
        """
        self.survey.is_public = False
        self.survey.save()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    def test_get_survey_id_is_private_user_is_not_create(self):
        """
        Prueba de obtener una encuesta con su id que es privada y el usuario no es su creador.
        """
        self.survey.is_public = False
        self.survey.save()
        self.client.force_authenticate(user=self.user_not_create)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_get_survey_id_without_token(self):
        """
        Prueba de obtener una encuesta con su id sin token.
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
