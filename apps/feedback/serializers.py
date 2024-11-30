from rest_framework import serializers
from .models import Comment, Qualify
from apps.surveys.models import Survey
from apps.users.serializers import UserResponseSerializer


class CommentValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'created_at', 'survey', 'user']
        read_only_fields = ['user']


    def validate_content(self, value):
        """
        Verifica que el contenido del comentario tenga mas de 10 caracteres.
        """
        if len(value) <= 10:
            raise serializers.ValidationError('Content must be more than 10 characters.')
        return value


    def create(self, validated_data):
        """
        Crea el comentario.
        """
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


    def update(self, instance, validated_data):
        """
        Actualiza el comentario.
        """
        instance.user = self.context['request'].user
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


class CommentResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'survey', 'user']


class QualifyValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualify
        fields = ['assessment', 'survey', 'user']


class QualifyResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer(read_only=True)

    class Meta:
        model = Qualify
        fields = ['id', 'assessment', 'survey', 'user']
