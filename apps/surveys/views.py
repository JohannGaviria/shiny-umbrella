from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import SurveyValidationSerializer, SurveyResponseSerializer
from apps.notification.utils import EmailNotification


# Endpoint para crear una encuesta
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_survey(request):
    # Serilaiza los datos
    survey_validation_serializer = SurveyValidationSerializer(data=request.data, context={'request': request})

    # Verifica que los datos sean válidos
    if not survey_validation_serializer.is_valid():
        # Respuesta de error en la validación de datos
        return Response({
            'status': 'error',
            'message': 'Errors in data validation.',
            'errors': survey_validation_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Guarda la encuesta
    survey = survey_validation_serializer.save()

    # Crea la url para ver la encuesta
    url = f'{settings.FRONTEND_URL}/api/surveys/{survey.id}'

    # Crea el mensaje de notificacion al crear la encuesta
    subject = f'Survey Created: "{survey.title}"'
    message = f'Hello {request.user.username},\n\nYour survey, "{survey.title}", has been created successfully. Access it here: {url}'
    recipient_list = [request.user.email]

    # Envia el mensaje al correo electrónico del usuario
    email_notification = EmailNotification(subject, message, recipient_list)
    email_notification.send()
    
    # Serializa los datos de respuesta de la encuesta
    survey_response_serializer = SurveyResponseSerializer(survey)

    # Respuesta exitosa al crear una encuesta
    return Response({
        'status': 'success',
        'message': 'Survey created successfully.',
        'data': {
            'survey': survey_response_serializer.data
        }
    }, status=status.HTTP_201_CREATED)

