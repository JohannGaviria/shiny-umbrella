from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from faker import Faker
from datetime import datetime, timedelta
import random


fake = Faker()


# Tests para la creación de encuestas
class SurveyCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create_survey')
        self.user = User.objects.create(
            username='TestUsername',
            email='test@email.com',
        )
        self.user.set_password('TestPassword')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.data = {
            'title': fake.sentence(nb_words=6),
            'description': fake.text(max_nb_chars=200),
            'end_date': datetime.now() + timedelta(days=random.randint(1, 30)),
            'is_public': random.choice([True, False])
        }


    def test_create_survey_successful(self):
        """
        Prueba de crear encuesta exitoso.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)
    

    def test_create_survey_successful_with_minimum_data(self):
        """
        Prueba de crear encuesta con los minimos datos
        """
        data = {
            'title': fake.sentence(nb_words=6),
            'end_date': datetime.now() + timedelta(days=random.randint(1, 30)),
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)
        

    def test_create_survey_without_title(self):
        """
        Prueba de crear una encuesta sin un título.
        """
        del self.data['title']
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)
    

    def test_create_survey_without_end_date(self):
        """
        Prueba de crear una encuesta sin fecha finalización.
        """
        del self.data['end_date']
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)
    

    def test_create_survey_description_too_short(self):
        """
        Prueba de crear una encuesta si la descripción es muy corta.
        """
        self.data['description'] = 'hello'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_create_survey_with_empty_description(self):
        """
        Prueba de crear encuesta sin una descripcion.
        """
        del self.data['description']
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    def test_create_survey_invalid_data(self):
        """
        Prueba de crear encuesta con datos invalidos.
        """
        self.data['is_public'] = 'asdfg'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_create_survey_start_date_in_past(self):
        """
        Prueba de crear una encuesta si start_date es una fecha pasada.
        """
        self.data['start_date'] = datetime.now() - timedelta(days=1)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_create_survey_end_date_before_start_date(self):
        """
        Prueba de crear una encuesta si end_date es anterior a start_date.
        """
        start_date = datetime.now() + timedelta(days=1)
        self.data['end_date'] = start_date - timedelta(days=1)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_create_survey_with_multiple_choice_question_without_enough_options(self):
        """
        Prueba de crear encuesta con pregunta de opción múltiple sin suficientes opciones.
        """
        self.data['asks'] = [{
            'text': '¿Cuál es tu color favorito?',
            'type': 'multiple',
            'options': [{'text': 'Rojo'}]
        }]
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_create_survey_with_short_question_with_options(self):
        """
        Prueba de crear encuesta con pregunta corta que tiene opciones.
        """
        self.data['asks'] = [{
            'text': '¿Cuál es tu nombre?',
            'type': 'short',
            'options': [{'text': 'N/A'}]
        }]
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)
    

    def test_create_survey_without_token(self):
        """
        Prueba de crear encuesta sin token.
        """
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
