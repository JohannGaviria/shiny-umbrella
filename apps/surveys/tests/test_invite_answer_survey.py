from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from apps.surveys.models import Survey, Ask, Option
from faker import Faker
from datetime import timedelta
import random


fake = Faker()


# Tests para invitar a responder las encuestas
class InviteAnswerSurveyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='TestUsername',
            email='test@email.com',
            password='TestPassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.user_not_create = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password()
        )
        self.survey = Survey.objects.create(
            title=fake.sentence(nb_words=6),
            description=fake.text(max_nb_chars=200),
            end_date=timezone.now() + timedelta(days=random.randint(1, 30)),
            is_public=True,
            user=self.user
        )
        self.url = reverse('invite_answer_survey', args=[self.survey.id])
        self.data = {
            "emails": [
                "invitee1@example.com",
                "invitee2@example.com",
                "invitee3@example.com"
            ]
        }


    def test_invite_answer_survey_successful(self):
        """
        Prueba de invitar a responder una encuesta exitosa.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_inviteanswer_survey_invalid_data(self):
        """
        Prueba de invitar a responder una encuesta con datos inválidos.
        """
        invalid_data = {}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_invite_answer_survey_not_found(self):
        """
        Prueba de invitar a responder una encuesta que no existe.
        """
        self.url = reverse('answer_survey', args=['ec7f051a960d42788a10ff51cc85dc23'])
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
    

    def test_invite_answer_survey_is_private_user_is_not_create(self):
        """
        Prueba de invitar a responder una encuesta que es privada y el usuario no es su creador.
        """
        self.survey.is_public = False
        self.survey.save()
        self.client.force_authenticate(user=self.user_not_create)
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_invite_answer_survey_without_token(self):
        """
        Prueba de invitar a responder una encuesta sin token.
        """
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)