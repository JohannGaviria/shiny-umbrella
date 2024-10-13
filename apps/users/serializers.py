from rest_framework import serializers
from django.contrib.auth.models import User


# Serializador para las respuestas en JSON
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'date_joined'
        ]