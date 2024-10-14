from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserValidationSerializer, UserResponseSerializer
from apps.notification.utils import EmailNotification


# Endpoint for user registration
@api_view(['POST'])
def sign_up(request):
    # Serializa los datos
    user_validation_serializer = UserValidationSerializer(data=request.data)

    # Verifica que los datos son válidos
    if user_validation_serializer.is_valid():
        # Guarda al nuevo usuario
        user = user_validation_serializer.save()

        # Crea un token de autenticación para el usuario
        token = Token.objects.create(user=user)

        # Serializa los datos del usuario
        user_response_serializer = UserResponseSerializer(user)

        # Crea el mensaje de correo electrónico
        subject = 'Welcome to Our Service'
        message = f'Hello {user.username},\n\nThank you for registering with our service.'
        recipient_list = [user.email]

        # Crear instancia de EmailNotification y enviar el correo
        email_notification = EmailNotification(subject, message, recipient_list)
        email_notification.send()

        # Respuesta exitosa desde el endpoint
        return Response({
            'status': 'success',
            'message': 'User registered successfully.',
            'data': {
                'token': {
                    'token_key': token.key
                },
                'user': user_response_serializer.data
            }
        }, status=status.HTTP_201_CREATED)
    
    # Respuesta erronea desde el endpoint
    return Response({
        'status': 'error',
        'message': 'Errors in data validation.',
        'errors': user_validation_serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# Endpoint for user login
@api_view(['POST'])
def sign_in(request):
    # Respuesta exitosa desde el endpoint
    return Response({
        'status': 'success',
        'message': 'User logged in successfully.'
    }, status=status.HTTP_200_OK)


# Endpoint for user logout
@api_view(['POST'])
def sign_out(request):
    # Respuesta exitosa desde el endpoint
    return Response({
        'status': 'success',
        'message': 'User logged out successfully.'
    }, status=status.HTTP_200_OK)


# Endpoint for updating user profile
@api_view(['PUT'])
def update_user(request):
    # Respuesta exitosa desde el endpoint
    return Response({
        'status': 'success',
        'message': 'User profile updated successfully.'
    }, status=status.HTTP_200_OK)


# Endpoint for deleting user
@api_view(['DELETE'])
def delete_user(request):
    # Respuesta exitosa desde el endpoint
    return Response({
        'status': 'success',
        'message': 'User deleted successfully.'
    }, status=status.HTTP_200_OK)
