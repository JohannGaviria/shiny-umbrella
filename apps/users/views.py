from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from .serializers import UserValidationSerializer, UserResponseSerializer, UserUpdateSerializer
from .utils import confirm_verification_token, generate_verification_token
from .models import VerifyAccount
from apps.notification.utils import EmailNotification
from datetime import timedelta


# Endpoint for user registration
@api_view(['POST'])
def sign_up(request):
    # Serializa los datos
    user_validation_serializer = UserValidationSerializer(data=request.data)

    # Verifica que los datos son válidos
    if user_validation_serializer.is_valid():
        # Guarda al nuevo usuario
        user = user_validation_serializer.save()

        # Crea el registro de verificación del usuario
        VerifyAccount.objects.create(user=user)

        # Desactiva la cuenta del usuario hasta su verificación
        user.is_active = False
        user.save()

        # Crea un token para la verifiación del email
        token_email = generate_verification_token(user.email)

        # Crea la URL para la verificación del email
        verification_url = f'{settings.FRONTEND_URL}/api/users/verify/{token_email}'

        # Crea el mensaje de verificación para el email
        subject = 'Verify your account'
        message = f'Hello {user.username},\n\nPlease click the link to verify your account: {verification_url}'
        recipient_list = [user.email]

        # Crea la instancia de EmailNotification y envia el correo
        email_notification = EmailNotification(subject, message, recipient_list)
        email_notification.send()

        # Crea un token de autenticación para el usuario
        token = Token.objects.create(user=user)

        # Serializa los datos del usuario
        user_response_serializer = UserResponseSerializer(user)

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


# Endpoint for user verify email
@api_view(['GET'])
def verify_email(request, token_email):
    # Confirma el token de verificación
    email = confirm_verification_token(token_email)

    # Verifica que el token sea válido
    if not email:
        # Respuesta erronea desde el endpoint
        return Response({
            'status': 'error',
            'message': 'Invalid or expired token.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Obtiene al usuario y el registro de verificación
        user = User.objects.get(email=email)
        verify_account = VerifyAccount.objects.get(user=user)

        # Verifica que el email ya este verificado
        if verify_account.email_verified:
            # Respuesta erronea desde el endpoint
            return Response({
                'status': 'error',
                'message': 'Email already verified.'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Activa al usuario
            user.is_active = True
            user.save()
            
            # Registra la verificación del email del usuario
            verify_account.email_verified = True
            verify_account.verifed_at = timezone.now()
            verify_account.save()
            
            # Crea el mensaje de bienvenidad para el email
            subject = 'Welcome to Our Service'
            message = f'Hello {user.username},\n\nThank you for registering with our service.'
            recipient_list = [user.email]

            # Crea la instancia de EmailNotification y envia el correo
            email_notification = EmailNotification(subject, message, recipient_list)
            email_notification.send()
            
            # Respuesta exitosa desde el endpoint
            return Response({
                'status': 'success',
                'message': 'Email verified successfully.'
            }, status=status.HTTP_200_OK)
    
    # No se encuentra al usuario
    except User.DoesNotExist:
        # Respuesta erronea desde el ednpoint
        return Response({
            'status': 'error',
            'message': 'User not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # No se encuetra el registro de verificación
    except VerifyAccount.DoesNotExist:
        # Respuesta erronea desde el endpoint
        return Response({
            'status': 'error',
            'message': 'Verification account not found.'
        }, status=status.HTTP_404_NOT_FOUND)


# Endpoint for user login
@api_view(['POST'])
def sign_in(request):
    # Obtiene los datos del usuario
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        # Busca al usuario que intenta iniciar sesión
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Respuesta erronea desde el endpoint
        return Response({
            'status': 'errors',
            'message': 'Validation failed',
            'errors': {
                'email': [
                    'Email is incorrect'
                ]
            }
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Verifica que la contraseña sea válida
    if not user.check_password(password):
        # Respuesta erronea desde el endpoint
        return Response({
            'status': 'errors',
            'message': 'Validation failed',
            'errors': {
                'password': [
                    'Password is incorrect'
                ]
            }
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Verifica que el usuario esté activado
    if not user.is_active:
        # Respuesta de error si el usuario no está activo
        return Response({
            'status': 'error',
            'message': 'The user is not active.'
        }, status=status.HTTP_403_FORBIDDEN)

    # Crea o actualiza el token del usuario
    token, created = Token.objects.get_or_create(user=user)

    # Configura el tiempo de expiración del token
    token_expiration = timezone.now() + timedelta(days=3)

    # Serializa los datos del usuario
    user_response_serializer = UserResponseSerializer(user)

    # Respuesta exitosa desde el endpoint
    return Response({
        'status': 'success',
        'message': 'User logged in successfully.',
        'data': {
            'token': {
                'token_key': token.key,
                'token_expiration': token_expiration.isoformat()
            },
            'user': user_response_serializer.data
        }
    }, status=status.HTTP_200_OK)


# Endpoint for user logout
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sign_out(request):
    # Elimina el token del usuario autenticado
    request.user.auth_token.delete()
    
    # Respuesta exitosa desde el endpoint
    return Response({
        'status': 'success',
        'message': 'User logged out successfully.'
    }, status=status.HTTP_200_OK)


# Endpoint for updating user profile
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    # Obtiene el usuario autenticado
    user = request.user
    
    # Serializa los datos
    user_update_serializer = UserUpdateSerializer(user, data=request.data, partial=True)

    # Verifica que los datos sean validos
    if user_update_serializer.is_valid():
        # Guarda los cambios del usuario
        user = user_update_serializer.save()

        # Crea el registro de verificación del usuario
        VerifyAccount.objects.create(user=user)

        # Desactiva la cuenta del usuario hasta su verificación
        user.is_active = False
        user.save()

        # Crea un token para la verifiación del email
        token_email = generate_verification_token(user.email)

        # Crea la URL para la verificación del email
        verification_url = f'{settings.FRONTEND_URL}/api/users/verify/{token_email}'

        # Crea el mensaje de verificación para el email
        subject = 'Verify your account'
        message = f'Hello {user.username},\n\nPlease click the link to verify your account: {verification_url}'
        recipient_list = [user.email]

        # Crea la instancia de EmailNotification y envia el correo
        email_notification = EmailNotification(subject, message, recipient_list)
        email_notification.send()

        # Elimina el token del usuario autenticado
        request.user.auth_token.delete()
        
        # Crea o actualiza el token del usuario
        token, created = Token.objects.get_or_create(user=user)

        # Configura el tiempo de expiración del token
        token_expiration = timezone.now() + timedelta(days=3)

        # Serializa los datos del usuario
        user_response_serializer = UserResponseSerializer(user)

        # Respuesta exitosa desde el endpoint
        return Response({
            'status': 'success',
            'message': 'User profile updated successfully.',
            'data': {
                'token': {
                    'token_key': token.key,
                    'token_expiration': token_expiration.isoformat()
                },
                'user': user_response_serializer.data
            }
        }, status=status.HTTP_200_OK)
    
    # Respuesta erronea desde el endpoint
    return Response({
        'status': 'error',
        'message': 'Errors in data validation.',
        'errors': user_update_serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# Endpoint for deleting user
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
    try:
        # Elimina el token del usuario autenticado
        request.user.auth_token.delete()

        # Elimina el usuario autenticado
        request.user.delete()

        # Respuesta exitosa desde el endpoint
        return Response({
            'status': 'success',
            'message': 'User deleted successfully.'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        # Respuesta erronea desde el endpoint
        return Response({
            'status': 'error',
            'message': 'Error deleting user.',
            'errors': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
