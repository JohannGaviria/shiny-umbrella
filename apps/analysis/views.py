from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.surveys.utils import get_survey_by_id
from .utils import *


# Endpoint para exportar los detalles del análisis
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def export_analysis_details(request, survey_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)

    # Verifica que el usuario es el creador
    if survey.user != request.user:
        # Respuesta errónea al usuario no ser el creador
        return Response({
            'status': 'error',
            'message': 'The user is not the creator of the survey.'
        }, status=status.HTTP_403_FORBIDDEN)

    # Respuesta exitosa a exportar el analisis
    return Response({
        'status': 'success',
        'message': 'Export of the analysis successfully.'
    }, status=status.HTTP_200_OK)
