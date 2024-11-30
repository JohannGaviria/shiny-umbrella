from django.db import models
from django.contrib.auth.models import User
from apps.surveys.models import Survey


# Definición del modelo de comentarios
class Comment(models.Model):
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')


# Definición del modelo de calificación
class Qualify(models.Model):
    ASSESSMENT_CHOICES = [
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Regular'),
        (4, 'Good'),
        (5, 'Very Good'),
    ]    
    assessment = models.IntegerField(choices=ASSESSMENT_CHOICES, null=False, blank=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='qualifies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qualifies')


    class Meta:
        unique_together = ('survey', 'user')
