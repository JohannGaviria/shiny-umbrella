from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db.models import Q
from .serializers import SurveyValidationSerializer, SurveyResponseSerializer, AnswerValidationSerializer, AnswerResponseSerializer
from .models import Survey, Invitation
from .utils import get_survey_by_id, check_survey_is_public, check_user_invited
from apps.notification.utils import EmailNotification
from apps.core.utils import CustomPageNumberPagination, validate_serializer, verify_user_is_creator
from config.settings.base import REST_FRAMEWORK


# Endpoint para crear una encuesta
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_survey(request):
    # Serilaiza los datos
    survey_validation_serializer = SurveyValidationSerializer(data=request.data, context={'request': request})

    # Obtiene la validación del serializer
    validation_error = validate_serializer(survey_validation_serializer)

    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)
    
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
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)

    # Verifica si la encuesta es pública
    if not check_survey_is_public(survey):
        # Verifica que el usuario sea el creador
        verification_result = verify_user_is_creator(survey, request.user, message='The user is not the creator of the survey.')
        if verification_result:
            # Respuesta erronea al usuario no ser el creador
            return Response(verification_result, status=status.HTTP_403_FORBIDDEN)
    
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
    surveys = Survey.objects.all().order_by('id')
    
    # Serializa los datos de respuesta de la encusta
    survey_response_serializer = SurveyResponseSerializer(surveys, many=True)

    # Crea la paginación de los datos obtenidos
    paginator = CustomPageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(surveys, request)

    # Serializa los datos de las encuestas
    survey_response_serializer = SurveyResponseSerializer(paginated_queryset, many=True)

    # Obtiene la respuesta con los datos paginados
    response_data = paginator.get_paginated_response(survey_response_serializer.data)

    # Respuesta exitosa al obtener las encuestas
    return Response({
        'status': 'success',
        'message': 'Surveys successfully obtained.',
        'data': {
            'page_info': {
                'count': response_data.data['count'],
                'page_size': int(request.query_params.get('page_size', REST_FRAMEWORK['PAGE_SIZE'])),
                'links': response_data.data['links']
            },
            'surveys': response_data.data['results']
        }
    }, status=status.HTTP_200_OK)


# Endpoint para la buscar encuestas
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
                'page_size': int(request.query_params.get('page_size', REST_FRAMEWORK['PAGE_SIZE'])),
                'links': response_data.data['links']
            },
            'surveys': response_data.data['results']
        }
    }, status=status.HTTP_200_OK)


# Endpoint para actualizar una encuesta
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_survey(request, survey_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica que el usuario sea el creador
    verification_result = verify_user_is_creator(survey, request.user, message='The user is not the creator of the survey.')
    if verification_result:
        # Respuesta erronea al usuario no ser el creador
        return Response(verification_result, status=status.HTTP_403_FORBIDDEN)
    
    # Serializa los datos de la encueta
    survey_validation_serializer = SurveyValidationSerializer(survey, data=request.data, partial=True)

    # Obtiene la validación del serializer
    validation_error = validate_serializer(survey_validation_serializer)

    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)
    
    # Actualiza la encuesta
    survey = survey_validation_serializer.save()

    # Serializa la respuesta
    survey_response_serializer = SurveyResponseSerializer(survey)

    # Respuesta exitosa al actualizar la encuesta
    return Response({
        'status': 'success',
        'message': 'Survey update successfully.',
        'data': {
            'survey': survey_response_serializer.data
        }
    }, status=status.HTTP_200_OK)


# Endpoint para eliminar una encuesta
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_survey(request, survey_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica que el usuario sea el creador
    verification_result = verify_user_is_creator(survey, request.user, message='The user is not the creator of the survey.')
    if verification_result:
        # Respuesta erronea al usuario no ser el creador
        return Response(verification_result, status=status.HTTP_403_FORBIDDEN)
    
    # Elimina la encuesta
    survey.delete()

    # Crea el mensaje de notificacion al crear la encuesta
    subject = f'Survey Delete: "{survey.title}"'
    message = f'Hello {request.user.username},\n\nYour survey, "{survey.title}", has been deleted successfully.'
    recipient_list = [request.user.email]

    # Envia el mensaje al correo electrónico del usuario
    email_notification = EmailNotification(subject, message, recipient_list)
    email_notification.send()

    # Respuesta exitosa al eliminar la encuesta
    return Response({
        'status': 'success',
        'message': 'Survey successfully deleted.'
    }, status=status.HTTP_200_OK)


# Endpoit para responder una encuesta
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def answer_survey(request, survey_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública y el usuario el creador
    if not check_survey_is_public(survey) and verify_user_is_creator(survey, request.user, message='You do not have permission to answer this survey.'):
        # Verifica si el usuario esta invitado
        user_not_invited = check_user_invited(survey, request.user.email)
        if isinstance(user_not_invited, dict) and user_not_invited.get('status') == 'error':
            # Respuesta erronea al usuario no cumplir la verificación
            return Response(user_not_invited, status=status.HTTP_403_FORBIDDEN)

    # Obtiene los datos de la solicitud
    answers_data = request.data.get('answers', [])

    # Verifica que existan datos
    if not answers_data:
        # Respuesta erronea al no haber datos
        return Response({
            'status': 'error',
            'message': 'No answers provided.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Valida y crea las respuestas de la encuesta
    answers = []
    for answer_data in answers_data:
        # Asigna el usuario autenticado a la respuesta
        answer_data['user'] = request.user.id

        # Serializa los datos de la respuesta
        answer_validation_serializer = AnswerValidationSerializer(data=answer_data)

        # Obtiene la validación del serializer
        validation_error = validate_serializer(answer_validation_serializer)

        # Verifica la validación del serializer
        if validation_error:
            # Respuesta de error en la validación del serializer
            return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)
        
        # Guarda la respuesta validada
        answer = answer_validation_serializer.save()
        answers.append(answer)

    # Crea el mensaje de notificacion a responder la encuesta
    subject = f'New Answer to Your Survey: "{survey.title}"'
    message = f'Hello {survey.user.username},\n\nYour survey, "{survey.title}", has received new responses.'
    recipient_list = [survey.user.email]
    
    # Envia el mensaje al correo electrónico del usuario
    email_notification = EmailNotification(subject, message, recipient_list)
    email_notification.send()

    # Serializa los datos para la respuesta
    answer_response_serializer = AnswerResponseSerializer(answers, many=True)

    # Respuesta exitosa al crear la respuestas
    return Response({
        'status': 'success',
        'message': 'Survey successfully answered.',
        'data': {
            'answers': answer_response_serializer.data
        }
    }, status=status.HTTP_201_CREATED)


# Endpoint para invitar a responder una encuesta
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def invite_answer_survey(request, survey_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)

    # Verifica que el usuario sea el creador
    verification_result = verify_user_is_creator(survey, request.user, message='You do not have permission to invite users to this survey.')
    if verification_result:
        # Respuesta erronea al usuario no ser el creador
        return Response(verification_result, status=status.HTTP_403_FORBIDDEN)

    # Obtiene la lista de correos electrónicos
    emails = request.data.get('emails', [])
    
    # Verifica que la lista no esté vacía
    if not emails:
        # Respuesta erronea al no haber correos electrónicos
        return Response({
            'status': 'error',
            'message': 'Emails are required.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verifica que todos los correos sean válidos y no estén vacíos
    for email in emails:
        if not email:
            return Response({
                'status': 'error',
                'message': 'All emails must be valid and not empty.'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # Crear invitaciones y enviar correos
    for email in emails:
        # Crea y guarda la invitación
        invitation = Invitation(survey=survey, email=email)
        invitation.save()

        # Crea la URL para responder la encuesta
        invite_url = f'{settings.FRONTEND_URL}/api/surveys/{survey_id}/answer'

        # Crea el mensaje de notificación para invitar al usuario
        subject = f'You are invited to participate in the survey: "{survey.title}"'
        message = f'Hello,\n\nYou have been invited to participate in the survey "{survey.title}".\n\nPlease follow the link below to participate:\n\n{invite_url}'
        recipient_list = [email]
        
        # Envia el mensaje al correo electrónico del usuario
        email_notification = EmailNotification(subject, message, recipient_list)
        email_notification.send()

    # Respuesta exitosa al enviar las invitaciones
    return Response({
        'status': 'success',
        'message': 'Invitations sent successfully.'
    }, status=status.HTTP_200_OK)
