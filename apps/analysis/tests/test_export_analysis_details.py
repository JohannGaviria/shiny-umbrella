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


# Tests para exportar los detalles del analisis
class ExportAnalysisDetailsTestsCase(TestCase):
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
        self.url = reverse('export_analysis_details', args=[self.survey.id])
    

    def test_export_analysis_details_successfully(self):
        """
        Prueba de exportar los detalles del analisis exitosamente.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)

    
    def test_export_analysis_details_survey_not_found(self):
        """
        Prueba de exportar los detalles del analisis de una encuesta que no existe.
        """
        self.url = reverse('export_analysis_details', args=['ec7f051a960d42788a10ff51cc85dc23'])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)

    
    def test_export_analysis_details_user_not_create(self):
        """
        Prueba de exportar los detalles del analisis de una encuesta que el usuario no es el creador.
        """
        self.client.force_authenticate(user=self.user_not_create)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)

    
    def test_export_analysis_details_without_token(self):
        """
        Prueba de exportar los detalles del analisis sin token.
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
