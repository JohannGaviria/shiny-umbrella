from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from apps.surveys.models import Survey
from apps.feedback.models import Qualify
from faker import Faker
from datetime import timedelta
import random


fake = Faker()


# Tests para actualizar una calificación de una encuesta
class UpdateQualifySurveyTestsCase(TestCase):
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
        self.user_not_create.set_password(fake.password())
        self.user_not_create.save()
        self.survey = Survey.objects.create(
            title=fake.sentence(nb_words=6),
            description=fake.text(max_nb_chars=200),
            end_date=timezone.now() + timedelta(days=random.randint(1, 30)),
            is_public=True,
            user=self.user
        )
        self.qualify = Qualify.objects.create(
            assessment=fake.random_int(min=1, max=5),
            user=self.user,
            survey=self.survey
        )
        self.url = reverse('update_qualify_survey', args=[self.survey.id, self.qualify.id])
        self.data = {
            "assessment": fake.random_int(min=1, max=5)
        }

    
    def test_update_qualify_survey_successful(self):
        """
        Prueba de actualizar una calificación de una encuesta exitosamente.
        """
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_update_qualify_survey_not_found(self):
        """
        Prueba de actualizar una calificación de una encuesta que no se encuentra.
        """
        url = reverse('update_qualify_survey', args=['ec7f051a960d42788a10ff51cc85dc23', self.qualify.id])
        response = self.client.put(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
    

    def test_update_qualify_survey_qualify_not_found(self):
        """
        Prueba de actualizar una calificación que no se encuentra de una encuesta.
        """
        url = reverse('update_qualify_survey', args=[self.survey.id, 9999])
        response = self.client.put(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_update_qualify_survey_is_private_user_is_not_create(self):
        """
        Prueba de actualizar una calificación de una encuesta que es privada y el usuario no es su creador.
        """
        self.survey.is_public = False
        self.survey.save()
        self.client.force_authenticate(user=self.user_not_create)
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)

    
    def test_add_qualify_survey_invalid_data(self):
        """
        Prueba de actualizar una calificación de una encuesta con los datos invalidos.
        """
        self.data['assessment'] = 'asd'
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_add_qualify_survey_without_token(self):
        """
        Prueba de actualizar una calificación de una encuesta sin token.
        """
        self.client.force_authenticate(user=None)
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
