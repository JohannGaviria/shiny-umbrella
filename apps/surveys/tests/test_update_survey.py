from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from apps.surveys.models import Survey
from faker import Faker
from datetime import datetime, timedelta
import random


fake = Faker()


# Tests para la actualización de encuesta
class UpdateSurveyTestsCase(TestCase):
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
        self.url = reverse('update_survey', args=[self.survey.id])
        self.data = {
            'title': fake.sentence(nb_words=6),
            'description': fake.text(max_nb_chars=200),
            'end_date': datetime.now() + timedelta(days=random.randint(1, 30)),
            'is_public': random.choice([True, False])
        }


    def test_update_survey_successful(self):
        """
        Prueba de actualizar encuesta exitoso.
        """
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)

    
    def test_update_survey_id_not_found(self):
        """
        Prueba de actualizar una encuesta con su id que no se encuentra.
        """
        url = reverse('update_survey', args=['ec7f051a960d42788a10ff51cc85dc23'])
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_update_survey_user_is_not_create(self):
        """
        Prueba de actualizar una encuesta que el usuario no es el creador.
        """
        self.client.force_authenticate(user=self.user_not_create)
        response = self.client.put(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
    

    def test_update_survey_description_too_short(self):
        """
        Prueba de actualizar una encuesta si la descripción es muy corta.
        """
        self.data['description'] = 'hello'
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_update_survey_invalid_data(self):
        """
        Prueba de actualizar una encuesta con datos invalidos.
        """
        self.data['is_public'] = 'asdfg'
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_update_survey_start_date_in_past(self):
        """
        Prueba de actualizar una encuesta si start_date es una fecha pasada.
        """
        self.data['start_date'] = datetime.now() - timedelta(days=1)
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_update_survey_end_date_before_start_date(self):
        """
        Prueba de actualizar una encuesta si end_date es anterior a start_date.
        """
        start_date = datetime.now() + timedelta(days=1)
        self.data['end_date'] = start_date - timedelta(days=1)
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_update_survey_with_multiple_choice_question_without_enough_options(self):
        """
        Prueba de actualizar una encuesta con pregunta de opción múltiple sin suficientes opciones.
        """
        self.data['asks'] = [{
            'text': '¿Cuál es tu color favorito?',
            'type': 'multiple',
            'options': [{'text': 'Rojo'}]
        }]
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_update_survey_with_short_question_with_options(self):
        """
        Prueba de actualizar una encuesta con pregunta corta que tiene opciones.
        """
        self.data['asks'] = [{
            'text': '¿Cuál es tu nombre?',
            'type': 'short',
            'options': [{'text': 'N/A'}]
        }]
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)
    

    def test_update_survey_without_token(self):
        """
        Prueba de actualizar encuesta sin token.
        """
        self.client.force_authenticate(user=None)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
