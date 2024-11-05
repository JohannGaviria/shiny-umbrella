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
import urllib.parse


fake = Faker()


# Tests para la buscar encuestas
class SearchSurveysTestsCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        base_url = reverse('search_surveys')
        query_params = {'query': fake.sentence(nb_words=6)}
        self.url = f"{base_url}?{urllib.parse.urlencode(query_params)}"
        self.user = User.objects.create(
            username='TestUsername',
            email='test@email.com',
        )
        self.user.set_password('TestPassword')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.survey = Survey.objects.create(
            title=fake.sentence(nb_words=6),
            description=fake.text(max_nb_chars=200),
            end_date=timezone.now() + timedelta(days=random.randint(1, 30)),
            is_public=True,
            user=self.user
        )

    
    def test_search_surveys_successful(self):
        """
        Prueba de buscar encuestas exitosamente.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)
    

    def test_search_surveys_without_parameter(self):
        """
        Prueba de buscar encuestas sin el párametro query
        """
        self.url = reverse('search_surveys')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_search_surveys_without_token(self):
        """
        Prueba de buscar encuestas sin token.
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
