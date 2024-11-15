from rest_framework import serializers
from django.utils import timezone
from .models import Survey, Option, Ask
from apps.users.serializers import UserResponseSerializer


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['text']


class AksSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)

    class Meta:
        model = Ask
        fields = ['text', 'type', 'options']


class SurveyValidationSerializer(serializers.ModelSerializer):
    description = serializers.CharField(min_length=10, required=False)
    asks = AksSerializer(many=True, required=False)

    class Meta:
        model = Survey
        fields = ['title', 'description', 'start_date', 'end_date', 'is_public', 'user', 'asks']
        read_only_fields = ['user']
    
    
    def validate_start_date(self, start_date):
        """
        Verifica que start_date no sea una fecha pasada.
        """
        if start_date < timezone.now():
            raise serializers.ValidationError('The start date cannot be a date in the past.')
        return start_date


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
            raise serializers.ValidationError('The end date must be greater than the start date.')
        
        return end_date
    

    def validate_asks(self, asks):
        """
        Verifica que las preguntas cumplan con las reglas.
        """
        for ask in asks:
            # Validación para preguntas de opción múltiple
            if ask.get('type') == 'multiple':
                options = ask.get('options', [])
                if len(options) < 2:
                    raise serializers.ValidationError("Multiple choice questions must have at least two options.")

            # Validación para preguntas de corta o verdadero/falso
            elif ask.get('type') in ['short', 'boolean']:
                if 'options' in ask and ask['options']:
                    raise serializers.ValidationError('Short or true/false questions should not have options.')
        
        return asks


    def create(self, validated_data):
        """
        Crea la encuesta
        """
        # Obtiene el usuario autenticado
        user = self.context['request'].user
        validated_data['user'] = user  # Asigna el usuario autenticado al campo 'user'
        
        # Extrae las preguntas anidadas del diccionario de datos validados
        asks_data = validated_data.pop('asks', [])

        # Crea la instancia de Survey con los datos validados (sin incluir 'asks')
        survey = super().create(validated_data)

        # Itera sobre cada pregunta (ask) proporcionada en la solicitud
        for ask_data in asks_data:
            options_data = ask_data.pop('options', [])  # Extrae las opciones anidadas
            ask = Ask.objects.create(survey=survey, **ask_data)  # Crea cada pregunta
            # Crea cada opción asociada a la pregunta actual
            for option_data in options_data:
                Option.objects.create(ask=ask, **option_data) # Crea cada opción

        return survey


    def update(self, instance, validated_data):
        """
        Actualiza la encuesta.
        """
        # Extrae los datos de las preguntas (asks) del diccionario de datos validados
        asks_data = validated_data.pop('asks', [])
        
        # Actualiza la instancia de la encuesta con los datos validados (sin incluir 'asks')
        instance = super().update(instance, validated_data)

        # Itera sobre cada pregunta proporcionada en la solicitud
        for ask_data in asks_data:
            # Extrae las opciones anidadas del diccionario de datos de la pregunta
            options_data = ask_data.pop('options', [])
            
            # Obtiene el ID de la pregunta si existe
            ask_id = ask_data.get('id')
            
            # Si la pregunta ya existe (tiene un ID)
            if ask_id:
                # Recupera la pregunta existente de la base de datos
                ask = Ask.objects.get(id=ask_id, survey=instance)
                
                # Actualiza los atributos de la pregunta existente
                for key, value in ask_data.items():
                    setattr(ask, key, value)
                
                # Guarda los cambios de la pregunta
                ask.save()
                
                # Itera sobre cada opción asociada a la pregunta actual
                for option_data in options_data:
                    # Obtiene el ID de la opción si existe
                    option_id = option_data.get('id')
                    
                    # Si la opción ya existe (tiene un ID)
                    if option_id:
                        # Recupera la opción existente de la base de datos
                        option = Option.objects.get(id=option_id, ask=ask)
                        
                        # Actualiza el texto de la opción existente
                        option.text = option_data.get('text', option.text)
                        
                        # Guarda los cambios de la opción
                        option.save()
                    else:
                        # Crea una nueva opción asociada a la pregunta actual
                        Option.objects.create(ask=ask, **option_data)
            else:
                # Si la pregunta no existe, crea una nueva pregunta
                ask = Ask.objects.create(survey=instance, **ask_data)
                
                # Itera sobre cada opción asociada a la nueva pregunta
                for option_data in options_data:
                    # Crea una nueva opción asociada a la nueva pregunta
                    Option.objects.create(ask=ask, **option_data)
        
        # Retorna la instancia actualizada de la encuesta
        return instance


class SurveyResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer(read_only=True)
    asks = AksSerializer(many=True, read_only=True)
    options = OptionSerializer(many=True, read_only=True)


    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'is_public', 'user', 'asks', 'options']
