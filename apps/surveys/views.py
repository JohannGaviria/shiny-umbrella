from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db.models import Q
from .serializers import SurveyValidationSerializer, SurveyResponseSerializer
from .models import Survey
from apps.notification.utils import EmailNotification
from apps.core.utils import CustomPageNumberPagination
from config.settings.base import REST_FRAMEWORK


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
    url = f'{settings.FRONTEND_URL}/api/surveys/get/{survey.id}'

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


# Endpoint para obtener una encuesta por ID
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_survey_id(request, survey_id):
    try:
        # Obtiene la encuesta mediante su ID
        survey = Survey.objects.get(id=survey_id)
    except Survey.DoesNotExist:
        # Respuesta erronea a no encontrar la encuesta
        return Response({
            'status': 'error',
            'message': 'Survey not found.'
        }, status=status.HTTP_404_NOT_FOUND)

    # Verifica que la encuesta sea privada
    if not survey.is_public:
        # Verifica que el usuario no sea creador
        if survey.user != request.user:
            # Respuesta erronea al usuario no ser el creador
            return Response({
                'status': 'error',
                'message': 'The user is not the creator of the survey.'
            }, status=status.HTTP_403_FORBIDDEN)
    
    # Serializa los datos de la encuesta
    survey_response_serializer = SurveyResponseSerializer(survey)

    # Respuesta exitosa al obtener una encuesta
    return Response({
        'status': 'success',
        'message': 'Survey successfully obtained.',
        'data': {
            'survey': survey_response_serializer.data
        }
    }, status=status.HTTP_200_OK)


# Endpoint para obtener todas las encuestas
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_surveys(request):
    # Obtiene todas las encuestas
    surveys = Survey.objects.all()
    
    # Serializa los datos de respuesta de la encusta
    survey_response_serializer = SurveyResponseSerializer(surveys, many=True)

    # Respuesta exitosa al obtener las encuestas
    return Response({
        'status': 'success',
        'message': 'Surveys successfully obtained.',
        'data': {
            'surveys': survey_response_serializer.data
        }
    }, status=status.HTTP_200_OK)


# Endpoint para la buscar encuestas por titulo
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_surveys(request):
    # Obtiene el párametro de búsqueda
    query = request.query_params.get('query', None)

    # Verifica que el párametro query es none
    if query is None:
        # Respuesta erronea a no proporcionar el párametro query
        return Response({
            'status': 'error',
            'message': 'The search parameter "query" is required.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Filtra las encuestas que coincidan con la búsqueda
    surveys = Survey.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(user__username__icontains=query)
    ).order_by('id')

    # Crea la paginación de los datos obtenidos
    paginator = CustomPageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(surveys, request)

    # Serializa los datos de las encuestas
    survey_response_serializer = SurveyResponseSerializer(paginated_queryset, many=True)

    # Obtiene la respuesta con los datos paginados
    response_data = paginator.get_paginated_response(survey_response_serializer.data)

    # Respuesta de exito a buscar las encuestas
    return Response({
        'status': 'success',
        'message': 'Searching for surveys successfully.',
        'data': {
            'page_info': {
                'count': response_data.data['count'],
                'page_size': request.query_params.get('page_size', REST_FRAMEWORK['PAGE_SIZE']),
                'links': response_data.data['links']
            },
            'surveys': response_data.data['results']
        }
    }, status=status.HTTP_200_OK)
