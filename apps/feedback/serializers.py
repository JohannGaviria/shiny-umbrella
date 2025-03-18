from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Comment, Qualify
from apps.users.serializers import UserResponseSerializer


class CommentValidationSerializer(serializers.ModelSerializer):
    """
    Serializador para la validación y creación de comentarios.
    """
    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Comment): Modelo de comentario.
            fields (list): Campos del serializador.
            read_only_fields (list): Campos de solo lectura.
        """
        model = Comment
        fields = ['content', 'created_at', 'survey', 'user']
        read_only_fields = ['user']


    def validate_content(self, value):
        """
        Verifica que el contenido del comentario tenga más de 10 caracteres.

        Args:
            value (str): Contenido del comentario a validar.

        Returns:
            str: Contenido del comentario validado.

        Raises:
            serializers.ValidationError: Si el contenido del comentario tiene 10 caracteres o menos.
        """
        if len(value) <= 10:
            raise serializers.ValidationError('Content must be more than 10 characters.')
        return value


    def create(self, validated_data):
        """
        Crea el comentario.

        Args:
            validated_data (dict): Datos validados para crear el comentario.

        Returns:
            Comment: Comentario creado.
        """
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


    def update(self, instance, validated_data):
        """
        Actualiza el comentario.

        Args:
            instance (Comment): Instancia del comentario a actualizar.
            validated_data (dict): Datos validados para actualizar el comentario.

        Returns:
            Comment: Comentario actualizado.
        """
        instance.user = self.context['request'].user
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


class CommentResponseSerializer(serializers.ModelSerializer):
    """
    Serializador para la respuesta de datos de comentario.
    """
    user = UserResponseSerializer(read_only=True)

    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Comment): Modelo de comentario.
            fields (list): Campos del serializador.
        """
        model = Comment
        fields = ['id', 'content', 'created_at', 'survey', 'user']


class QualifyValidationSerializer(serializers.ModelSerializer):
    """
    Serializador para la validación y creación de calificaciones.
    """
    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Qualify): Modelo de calificación.
            fields (list): Campos del serializador.
            read_only_fields (list): Campos de solo lectura.
        """
        model = Qualify
        fields = ['assessment', 'survey', 'user']
        read_only_fields = ['user']
    

    def validate(self, data):
        """
        Valida que el usuario no haya calificado ya la encuesta.

        Args:
            data (dict): Datos a validar.

        Returns:
            dict: Datos validados.

        Raises:
            ValidationError: Si el usuario ya ha calificado la encuesta.
        """
        user = self.context['request'].user
        survey = data.get('survey')
        if Qualify.objects.filter(survey=survey, user=user).exists():
            raise ValidationError({
                'qualify': 'The user has already rated this survey.'
            })    
        return data
    

    def create(self, validated_data):
        """
        Crea la calificación.

        Args:
            validated_data (dict): Datos validados para crear la calificación.

        Returns:
            Qualify: Calificación creada.
        """
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


    def update(self, instance, validated_data):
        """
        Actualiza la calificación.

        Args:
            instance (Qualify): Instancia de la calificación a actualizar.
            validated_data (dict): Datos validados para actualizar la calificación.

        Returns:
            Qualify: Calificación actualizada.
        """
        instance.user = self.context['request'].user
        instance.assessment = validated_data.get('assessment', instance.assessment)
        instance.save()
        return instance


class QualifyResponseSerializer(serializers.ModelSerializer):
    """
    Serializador para la respuesta de datos de calificación.
    """
    user = UserResponseSerializer(read_only=True)

    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Qualify): Modelo de calificación.
            fields (list): Campos del serializador.
        """
        model = Qualify
        fields = ['id', 'assessment', 'survey', 'user']
