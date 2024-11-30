from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.surveys.models import Survey
from .serializers import CommentValidationSerializer


# Endpoint para agregar un comentario a una encuesta
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_comment_survey(request, survey_id):
    try:
        # Busca la encuesta mediante su ID
        survey = Survey.objects.get(id=survey_id)
    except Survey.DoesNotExist:
        # Respuesta erronea al no encontrar la encuesta
        return Response({
            'status': 'error',
            'message': 'Survey not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica que el usuario sea el creador
    if survey.user != request.user:
        # Respuesta erronea al usuario no ser el creador
        return Response({
            'status': 'error',
            'message': 'You do not have permission to comment on the survey.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Agrega el ID de la encuesta a los datos
    request.data['survey'] = survey_id

    # Serializa los datos para la validación
    comment_validation_serializer = CommentValidationSerializer(data=request.data, context={'request': request})

    # Verifica que los datos son válidos
    if not comment_validation_serializer.is_valid():
        # Respuesta de error en la validación de datos
        return Response({
            'status': 'error',
            'message': 'Errors in data validation.',
            'errors': comment_validation_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Guarda el comentario
    comment_validation_serializer.save()
    
    # Respuesta exitosa a agregar un comentario
    return Response({
        'status': 'success',
        'message': 'Comment added successfully.'
    }, status=status.HTTP_201_CREATED)
