from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Definición del modelo de verificación de cuenta
class VerifyAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    verifed_at = models.DateTimeField(default=timezone.now, null=False)
