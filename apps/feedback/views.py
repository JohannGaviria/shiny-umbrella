from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.surveys.models import Survey, Invitation
from apps.core.utils import CustomPageNumberPagination
from config.settings.base import REST_FRAMEWORK
from .serializers import CommentValidationSerializer, CommentResponseSerializer, QualifyValidationSerializer
from .models import Comment


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
    
    # Verifica si la encuesta es pública o privada
    if not survey.is_public and survey.user != request.user:
        # Verifica que el usuario este invitado a responder la encuesta
        invitation = Invitation.objects.filter(survey=survey, email=request.user.email).first()
        if not invitation:
            # Respuesta erronea al usuario no tener permiso
            return Response({
                'status': 'error',
                'message': 'You do not have permission to answer this survey.'
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


#Endpoint para obtener todos los comentatios de una encuesta
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_comments_survey(request, survey_id):
    try:
        # Busca la encuesta por su ID
        survey = Survey.objects.get(id=survey_id)
    except Survey.DoesNotExist:
        # Respuesta erronea al no encontrar la encuesta
        return Response({
            'status': 'error',
            'message': 'Survey not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública o privada
    if not survey.is_public and survey.user != request.user:
        # Verifica que el usuario este invitado a responder la encuesta
        invitation = Invitation.objects.filter(survey=survey, email=request.user.email).first()
        if not invitation:
            # Respuesta erronea al usuario no tener permiso
            return Response({
                'status': 'error',
                'message': 'You do not have permission to answer this survey.'
            }, status=status.HTTP_403_FORBIDDEN)
        
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
    try:
        # Busca la encuesta por su ID
        survey = Survey.objects.get(id=survey_id)
    except Survey.DoesNotExist:
        # Respuesta erronea al no encontrar la encuesta
        return Response({
            'status': 'error',
            'message': 'Survey not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública o privada
    if not survey.is_public and survey.user != request.user:
        # Verifica que el usuario este invitado a responder la encuesta
        invitation = Invitation.objects.filter(survey=survey, email=request.user.email).first()
        if not invitation:
            # Respuesta erronea al usuario no tener permiso
            return Response({
                'status': 'error',
                'message': 'You are not allowed to comment on the survey.'
            }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Busca el comentario de la encuesta por su ID
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        # Respuesta erronea al no encontrar la encuesta
        return Response({
            'status': 'error',
            'message': 'Comment not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica que el usuario es el creador
    if comment.user != request.user:
        # Respuesta erronea al usuario no ser el creador del comentario
        return Response({
            'status': 'error',
            'message': 'The user is not the creator of the comment.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Serializa los datos del comentario
    comment_validation_serializer = CommentValidationSerializer(
        comment,
        data=request.data,
        partial=True,
        context={'request': request}
    )

    # Verifica que los datos sean válidos
    if not comment_validation_serializer.is_valid():
        # Respuesta erronea en la validación de los datos
        return Response({
            'status': 'error',
            'message': 'Errors in data validation.',
            'errors': comment_validation_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

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
    try:
        # Busca la encuesta por su ID
        survey = Survey.objects.get(id=survey_id)
    except Survey.DoesNotExist:
        # Respuesta erronea al no encontrar la encuesta
        return Response({
            'status': 'error',
            'message': 'Survey not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública o privada
    if not survey.is_public and survey.user != request.user:
        # Verifica que el usuario este invitado a responder la encuesta
        invitation = Invitation.objects.filter(survey=survey, email=request.user.email).first()
        if not invitation:
            # Respuesta erronea al usuario no tener permiso
            return Response({
                'status': 'error',
                'message': 'You are not allowed to comment on the survey.'
            }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Busca el comentario de la encuesta por su ID
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        # Respuesta erronea al no encontrar la encuesta
        return Response({
            'status': 'error',
            'message': 'Comment not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica que el usuario es el creador
    if comment.user != request.user:
        # Respuesta erronea al usuario no ser el creador del comentario
        return Response({
            'status': 'error',
            'message': 'The user is not the creator of the comment.'
        }, status=status.HTTP_403_FORBIDDEN)
    
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
    try:
        # Busca la encuesta por su ID
        survey = Survey.objects.get(id=survey_id)
    except Survey.DoesNotExist:
        # Respuesta erronea al no encontrar la encuesta
        return Response({
            'status': 'error',
            'message': 'Survey not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica si la encuesta es pública o privada
    if not survey.is_public and survey.user != request.user:
        # Verifica que el usuario este invitado a responder la encuesta
        invitation = Invitation.objects.filter(survey=survey, email=request.user.email).first()
        if not invitation:
            # Respuesta erronea al usuario no tener permiso
            return Response({
                'status': 'error',
                'message': 'You are not allowed to qualify on the survey.'
            }, status=status.HTTP_403_FORBIDDEN)
    
    # Agrega el ID de la encuesta a los datos
    request.data['survey'] = survey_id

    # Serializa los datos para la validación
    qualify_validation_serializer = QualifyValidationSerializer(data=request.data, context={'request': request})

    # Verifica que los datos son válidos
    if not qualify_validation_serializer.is_valid():
        # Respuesta de error en la validación de datos
        return Response({
            'status': 'error',
            'message': 'Errors in data validation.',
            'errors': qualify_validation_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Guarda la calificación
    qualify_validation_serializer.save()
    
    # Respuesta exitosa a agregar una calificación
    return Response({
        'status': 'success',
        'message': 'Qualify added successfully.'
    }, status=status.HTTP_201_CREATED)
