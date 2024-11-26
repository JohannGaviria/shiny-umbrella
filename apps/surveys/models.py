from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4


# Definición del modelo de encuestas
class Survey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)
    is_public = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys')


# Definición del modelo de pregunta de la encuesta
class Ask(models.Model):
    TYPE_CHOICES = [
        ('multiple', 'Multiple Choice'),
        ('short', 'Short Answer'),
        ('boolean', 'True/False'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    text = models.CharField(max_length=255, null=False, blank=False)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=False, blank=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='asks')


# Definición del modelo de opciones de respuesta de la encuesta
class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    text = models.CharField(max_length=255, null=False, blank=False)
    ask = models.ForeignKey(Ask, on_delete=models.CASCADE, related_name='options')


# Definición del modelo de respuesta
class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    content_answer = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    ask = models.ForeignKey(Ask, on_delete=models.CASCADE, related_name='answers')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='answers', blank=True, null=True)


    class Meta:
        unique_together = ('user', 'ask') # Asegura que el mismo usuario no responda dos veces


# Definición del modelo de invitación
class Invitation(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    email = models.EmailField()
    invited_at = models.DateTimeField(auto_now_add=True)
