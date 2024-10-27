from rest_framework import serializers
from django.utils import timezone
from .models import Survey
from apps.users.serializers import UserResponseSerializer


class SurveyValidationSerializer(serializers.ModelSerializer):
    description = serializers.CharField(min_length=10, required=False)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'is_public', 'user']
        read_only_fields = ['user']
    
    
    def validate_end_date(self, end_date):
        """
        Verifica que end_date sea mayor que start_date
        """
        start_date_field = Survey._meta.get_field('start_date')
        start_date = start_date_field.default() if callable(start_date_field.default) else start_date_field.default

        # Asegúrate de que start_date sea un objeto de fecha
        if isinstance(start_date, str):
            start_date = timezone.datetime.fromisoformat(start_date)

        if end_date <= start_date:
            raise serializers.ValidationError("The end date must be greater than the start date.")
        
        return end_date
    

    def create(self, validated_data):
        # Obtiene el usuario autenticado
        user = self.context['request'].user
        validated_data['user'] = user  # Asigna el usuario autenticado al campo 'user'
        
        # Crea la instancia de Survey con los datos validados
        return super().create(validated_data)


class SurveyResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer(read_only=True)
    class Meta:
        model = Survey
        fields = '__all__'
