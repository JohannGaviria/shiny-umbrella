from rest_framework import serializers
from django.utils import timezone
from .models import Survey, Option, Ask, Answer
from apps.users.serializers import UserResponseSerializer


class OptionSerializer(serializers.ModelSerializer):
    """
    Serializador para las opciones de las preguntas.
    """
    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Option): Modelo de opción.
            fields (list): Campos del serializador.
        """
        model = Option
        fields = ['id', 'text']


class AksSerializer(serializers.ModelSerializer):
    """
    Serializador para las preguntas de las encuestas.
    """
    options = OptionSerializer(many=True, required=False)

    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Ask): Modelo de pregunta.
            fields (list): Campos del serializador.
        """
        model = Ask
        fields = ['id', 'text', 'type', 'options']


class SurveyValidationSerializer(serializers.ModelSerializer):
    """
    Serializador para la validación y creación de encuestas.
    """
    description = serializers.CharField(min_length=10, required=False)
    asks = AksSerializer(many=True, required=False)

    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Survey): Modelo de encuesta.
            fields (list): Campos del serializador.
            read_only_fields (list): Campos de solo lectura.
        """
        model = Survey
        fields = ['title', 'description', 'start_date', 'end_date', 'is_public', 'user', 'asks']
        read_only_fields = ['user']
    
    
    def validate_start_date(self, start_date):
        """
        Verifica que start_date no sea una fecha pasada.

        Args:
            start_date (datetime): Fecha de inicio a validar.

        Returns:
            datetime: Fecha de inicio validada.

        Raises:
            serializers.ValidationError: Si la fecha de inicio es una fecha pasada.
        """
        if start_date < timezone.now():
            raise serializers.ValidationError('The start date cannot be a date in the past.')
        return start_date


    def validate_end_date(self, end_date):
        """
        Verifica que end_date sea mayor que start_date.

        Args:
            end_date (datetime): Fecha de finalización a validar.

        Returns:
            datetime: Fecha de finalización validada.

        Raises:
            serializers.ValidationError: Si la fecha de finalización no es mayor que la fecha de inicio.
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

        Args:
            asks (list): Lista de preguntas a validar.

        Returns:
            list: Lista de preguntas validadas.

        Raises:
            serializers.ValidationError: Si alguna pregunta no cumple con las reglas.
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
        Crea la encuesta.

        Args:
            validated_data (dict): Datos validados para crear la encuesta.

        Returns:
            Survey: Encuesta creada.
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

        Args:
            instance (Survey): Instancia de la encuesta a actualizar.
            validated_data (dict): Datos validados para actualizar la encuesta.

        Returns:
            Survey: Encuesta actualizada.
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
    """
    Serializador para la respuesta de datos de encuesta.
    """
    user = UserResponseSerializer(read_only=True)
    asks = AksSerializer(many=True, read_only=True)
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Survey): Modelo de encuesta.
            fields (list): Campos del serializador.
        """
        model = Survey
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'is_public', 'user', 'asks', 'options']


class AnswerValidationSerializer(serializers.ModelSerializer):
    """
    Serializador para la validación y creación de respuestas.
    """
    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Answer): Modelo de respuesta.
            fields (list): Campos del serializador.
        """
        model = Answer
        fields = ['content_answer', 'user', 'ask', 'option']
    

    def validate(self, data):
        """
        Valida los datos de la respuesta.

        Args:
            data (dict): Datos a validar.

        Returns:
            dict: Datos validados.

        Raises:
            serializers.ValidationError: Si alguna validación falla.
        """
        # Verificar que la encuesta está activa (start_date <= now <= end_date)
        ask = data.get('ask')
        if ask:
            survey = ask.survey
            now = timezone.now()
            if not (survey.start_date <= now <= survey.end_date):
                raise serializers.ValidationError("The survey is not active.")
        
        # Validar las opciones de respuesta según el tipo de pregunta
        ask_type = ask.type
        content_answer = data.get('content_answer')
        option = data.get('option')

        if ask_type == 'multiple':
            if not option:
                raise serializers.ValidationError("Multiple choice questions require an option to be selected.")
        elif ask_type in ['short', 'boolean']:
            if option:
                raise serializers.ValidationError(f"{ask_type.capitalize()} questions should not have options.")
            if ask_type == 'boolean' and content_answer not in ['True', 'False']:
                raise serializers.ValidationError("Boolean questions require a True or False answer.")
        
        return data


class AnswerResponseSerializer(serializers.ModelSerializer):
    """
    Serializador para la respuesta de datos de respuesta.
    """
    user = UserResponseSerializer(read_only=True)
    ask = AksSerializer(read_only=True)
    option = OptionSerializer(read_only=True)

    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Answer): Modelo de respuesta.
            fields (list): Campos del serializador.
        """
        model = Answer
        fields = ['id', 'user', 'ask', 'content_answer', 'option']
