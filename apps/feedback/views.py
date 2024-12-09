from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.surveys.models import Invitation
from apps.core.utils import CustomPageNumberPagination, validate_serializer, verify_user_is_creator
from apps.surveys.utils import get_survey_by_id, check_user_invited, check_survey_is_public
from config.settings.base import REST_FRAMEWORK
from .serializers import CommentValidationSerializer, CommentResponseSerializer, QualifyValidationSerializer, QualifyResponseSerializer
from .models import Comment, Qualify


# Endpoint para agregar un comentario a una encuesta
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_comment_survey(request, survey_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública
    if not check_survey_is_public(survey):
        # Verifica si el usuario esta invitado
        user_not_invited = check_user_invited(survey, request.user.email)
        if isinstance(user_not_invited, dict) and survey.get('status') == 'error':
            # Respuesta erronea al usuario no cumplir la verificación
            return Response(user_not_invited, status=status.HTTP_403_FORBIDDEN)
    
    # Agrega el ID de la encuesta a los datos
    request.data['survey'] = survey_id

    # Serializa los datos para la validación
    comment_validation_serializer = CommentValidationSerializer(data=request.data, context={'request': request})

    # Obtiene la validación del serializer
    validation_error = validate_serializer(comment_validation_serializer)

    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)
    
    # Guarda el comentario
    comment_validation_serializer.save()
    
    # Respuesta exitosa a agregar un comentario
    return Response({
        'status': 'success',
        'message': 'Comment added successfully.'
    }, status=status.HTTP_201_CREATED)


#Endpoint para obtener todos los comentatios de una encuesta
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_comments_survey(request, survey_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública y el usuario el creador
    if not check_survey_is_public(survey) and verify_user_is_creator(survey, request.user, message='You do not have permission to comment this survey.'):
        # Verifica si el usuario esta invitado
        user_not_invited = check_user_invited(survey, request.user.email)
        if isinstance(user_not_invited, dict) and survey.get('status') == 'error':
            # Respuesta erronea al usuario no cumplir la verificación
            return Response(user_not_invited, status=status.HTTP_403_FORBIDDEN)
        
    # Obtiene todos los comentarios de la encuesta
    comments = Comment.objects.filter(survey=survey.id).order_by('id')

    # Crea la paginación de los datos obtenidos
    paginator = CustomPageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(comments, request)

    # Serializa los datos de los comentarios
    comment_response_serializer = CommentResponseSerializer(paginated_queryset, many=True)

    # Obtiene la respuesta con los datos paginados
    response_data = paginator.get_paginated_response(comment_response_serializer.data)

    # Respuesta exitosa al obtener las encuestas
    return Response({
        'status': 'success',
        'message': 'Comments successfully obtained.',
        'data': {
            'page_info': {
                'count': response_data.data['count'],
                'page_size': int(request.query_params.get('page_size', REST_FRAMEWORK['PAGE_SIZE'])),
                'links': response_data.data['links']
            },
            'comments': response_data.data['results']
        }
    }, status=status.HTTP_200_OK)


# Endpoint para actualizar un comentario de una encuesta
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_comment_survey(request, survey_id, comment_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública
    if not check_survey_is_public(survey):
        # Verifica si el usuario esta invitado
        user_not_invited = check_user_invited(survey, request.user.email)
        if isinstance(user_not_invited, dict) and survey.get('status') == 'error':
            # Respuesta erronea al usuario no cumplir la verificación
            return Response(user_not_invited, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Busca el comentario de la encuesta por su ID
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        # Respuesta erronea al no encontrar la encuesta
        return Response({
            'status': 'error',
            'message': 'Comment not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica que el usuario sea el creador
    verification_result = verify_user_is_creator(comment, request.user, message='The user is not the creator of the comment.')
    if verification_result:
        # Respuesta erronea al usuario no ser el creador
        return Response(verification_result, status=status.HTTP_403_FORBIDDEN)
    
    # Serializa los datos del comentario
    comment_validation_serializer = CommentValidationSerializer(
        comment,
        data=request.data,
        partial=True,
        context={'request': request}
    )

    # Obtiene la validación del serializer
    validation_error = validate_serializer(comment_validation_serializer)

    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)

    # Actualiza el comentario de la encuesta
    comment_validation_serializer.save()

    # Respuesta exitosa al actualizar el comentario
    return Response({
        'status': 'success',
        'message': 'Comment update successfully.'
    }, status=status.HTTP_200_OK)


# Endpoint para eliminar un comentario de una encuesta
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_comment_survey(request, survey_id, comment_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública
    if not check_survey_is_public(survey):
        # Verifica si el usuario esta invitado
        user_not_invited = check_user_invited(survey, request.user.email)
        if isinstance(user_not_invited, dict) and survey.get('status') == 'error':
            # Respuesta erronea al usuario no cumplir la verificación
            return Response(user_not_invited, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Busca el comentario de la encuesta por su ID
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        # Respuesta erronea al no encontrar la encuesta
        return Response({
            'status': 'error',
            'message': 'Comment not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica que el usuario sea el creador
    verification_result = verify_user_is_creator(comment, request.user, message='The user is not the creator of the comment.')
    if verification_result:
        # Respuesta erronea al usuario no ser el creador
        return Response(verification_result, status=status.HTTP_403_FORBIDDEN)
    
    # Elimina el comentario de la encuesta
    comment.delete()

    # Respuesta exitosa al eliminar el commentario
    return Response({
        'status': 'success',
        'message': 'Comment successfully deleted.'
    }, status=status.HTTP_200_OK)


# Endpoint para agregar una calificación a una encuesta
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_qualify_survey(request, survey_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública
    if not check_survey_is_public(survey):
        # Verifica si el usuario esta invitado
        user_not_invited = check_user_invited(survey, request.user.email)
        if isinstance(user_not_invited, dict) and survey.get('status') == 'error':
            # Respuesta erronea al usuario no cumplir la verificación
            return Response(user_not_invited, status=status.HTTP_403_FORBIDDEN)
    
    # Agrega el ID de la encuesta a los datos
    request.data['survey'] = survey_id

    # Serializa los datos para la validación
    qualify_validation_serializer = QualifyValidationSerializer(data=request.data, context={'request': request})

    # Obtiene la validación del serializer
    validation_error = validate_serializer(qualify_validation_serializer)

    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)
    
    # Guarda la calificación
    qualify_validation_serializer.save()
    
    # Respuesta exitosa a agregar una calificación
    return Response({
        'status': 'success',
        'message': 'Qualify added successfully.'
    }, status=status.HTTP_201_CREATED)


#Endpoint para obtener todas las calificaciones de una encuesta
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_qualifies_survey(request, survey_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública y el usuario el creador
    if not check_survey_is_public(survey) and verify_user_is_creator(survey, request.user, message='You do not have permission to rate this survey.'):
        # Verifica si el usuario esta invitado
        user_not_invited = check_user_invited(survey, request.user.email)
        if isinstance(user_not_invited, dict) and survey.get('status') == 'error':
            # Respuesta erronea al usuario no cumplir la verificación
            return Response(user_not_invited, status=status.HTTP_403_FORBIDDEN)
        
    # Obtiene todas las calificaciones de la encuesta
    qualifies = Qualify.objects.filter(survey=survey.id).order_by('id')

    # Crea la paginación de los datos obtenidos
    paginator = CustomPageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(qualifies, request)

    # Serializa los datos de las calificaciones
    qualify_response_serializer = QualifyResponseSerializer(paginated_queryset, many=True)

    # Obtiene la respuesta con los datos paginados
    response_data = paginator.get_paginated_response(qualify_response_serializer.data)

    # Respuesta exitosa al obtener las encuestas
    return Response({
        'status': 'success',
        'message': 'Qualifies successfully obtained.',
        'data': {
            'page_info': {
                'count': response_data.data['count'],
                'page_size': int(request.query_params.get('page_size', REST_FRAMEWORK['PAGE_SIZE'])),
                'links': response_data.data['links']
            },
            'qualifies': response_data.data['results']
        }
    }, status=status.HTTP_200_OK)


# Endpoint para actualizar una calificación de una encuesta
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_qualify_survey(request, survey_id, qualify_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública
    if not check_survey_is_public(survey):
        # Verifica si el usuario esta invitado
        user_not_invited = check_user_invited(survey, request.user.email)
        if isinstance(user_not_invited, dict) and survey.get('status') == 'error':
            # Respuesta erronea al usuario no cumplir la verificación
            return Response(user_not_invited, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Busca la calificación de la encuesta por su ID
        qualify = Qualify.objects.get(id=qualify_id)
    except Qualify.DoesNotExist:
        # Respuesta erronea al no encontrar la calificación
        return Response({
            'status': 'error',
            'message': 'Qualify not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica que el usuario sea el creador
    verification_result = verify_user_is_creator(qualify, request.user, message='The user is not the creator of the rating.')
    if verification_result:
        # Respuesta erronea al usuario no ser el creador
        return Response(verification_result, status=status.HTTP_403_FORBIDDEN)
    
    # Serializa los datos de la calificación
    qualify_validation_serializer = QualifyValidationSerializer(
        qualify,
        data=request.data,
        partial=True,
        context={'request': request}
    )

    # Obtiene la validación del serializer
    validation_error = validate_serializer(qualify_validation_serializer)

    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)

    # Actualiza el comentario de la encuesta
    qualify_validation_serializer.save()

    # Respuesta exitosa al actualizar el comentario
    return Response({
        'status': 'success',
        'message': 'Qualify updated successfully.'
    }, status=status.HTTP_200_OK)


# Endpoint para eliminar una calificación de una encuesta
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_qualify_survey(request, survey_id, qualify_id):
    # Obtiene la respuesta
    survey = get_survey_by_id(survey_id)

    # Comprueba si la función devolvió un diccionario de error
    if isinstance(survey, dict) and survey.get('status') == 'error':
        # Respuesta erronea al no encontrar la encuesta
        return Response(survey, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública
    if not check_survey_is_public(survey):
        # Verifica si el usuario esta invitado
        user_not_invited = check_user_invited(survey, request.user.email)
        if isinstance(user_not_invited, dict) and survey.get('status') == 'error':
            # Respuesta erronea al usuario no cumplir la verificación
            return Response(user_not_invited, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Busca la calificación de la encuesta por su ID
        qualify = Qualify.objects.get(id=qualify_id)
    except Qualify.DoesNotExist:
        # Respuesta erronea al no encontrar la califiación
        return Response({
            'status': 'error',
            'message': 'Qualify not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica que el usuario sea el creador
    verification_result = verify_user_is_creator(qualify, request.user, message='The user is not the creator of the rating.')
    if verification_result:
        # Respuesta erronea al usuario no ser el creador
        return Response(verification_result, status=status.HTTP_403_FORBIDDEN)
    
    # Elimina la califiación de la encuesta
    qualify.delete()

    # Respuesta exitosa al eliminar la calificación
    return Response({
        'status': 'success',
        'message': 'Qualify successfully deleted.'
    }, status=status.HTTP_200_OK)
