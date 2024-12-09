from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from .serializers import UserValidationSerializer, UserResponseSerializer, UserUpdateSerializer
from .utils import confirm_verification_token, generate_verification_token
from .models import VerifyAccount
from apps.notification.utils import EmailNotification
from apps.core.utils import validate_serializer
from datetime import timedelta


# Endpoint para el registro de usuario
@api_view(['POST'])
def sign_up(request):
    # Serializa los datos
    user_validation_serializer = UserValidationSerializer(data=request.data)

    # Obtiene la validación del serializer
    validation_error = validate_serializer(user_validation_serializer)

    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)
    
    # Guarda al nuevo usuario
    user = user_validation_serializer.save()

    # Crea o obtiene el registro de verificación del usuario
    verify_account, created = VerifyAccount.objects.get_or_create(user=user)

    # Desactiva la cuenta del usuario hasta su verificación
    user.is_active = False
    user.save()

    # Crea un token para la verifiación del correo electrónico
    token_email = generate_verification_token(user.email)

    # Crea la URL para la verificación del correo electrónico
    verification_url = f'{settings.FRONTEND_URL}/api/users/verify/{token_email}'

    # Crea el mensaje de verificación del correo electrónico
    subject = 'Verify your account'
    message = f'Hello {user.username},\n\nPlease click the link to verify your account: {verification_url}'
    recipient_list = [user.email]

    # Envia el mensaje al correo electrónico del usuario
    email_notification = EmailNotification(subject, message, recipient_list)
    email_notification.send()

    # Crea un token de autenticación para el usuario
    token = Token.objects.create(user=user)

    # Serializa los datos del usuario
    user_response_serializer = UserResponseSerializer(user)

    # Respuesta de registro de usuario exitoso
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


# Endpoint para la verificación del correo electrónico de usuario
@api_view(['GET'])
def verify_email(request, token_email):
    # Confirma el token de verificación
    email = confirm_verification_token(token_email)

    # Verifica que el token sea válido
    if not email:
        # Respuesta de error en la verificación del token
        return Response({
            'status': 'error',
            'message': 'Invalid or expired token.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Obtiene al usuario y el registro de verificación
        user = User.objects.get(email=email)
        verify_account = VerifyAccount.objects.get(user=user)

        # Verifica que el correo electrónico este verificado
        if verify_account.email_verified:
            # Respuesta de error por correo electrónico ya verificado
            return Response({
                'status': 'error',
                'message': 'Email already verified.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Activa al usuario
        user.is_active = True
        user.save()
        
        # Registra la verificación del correo electrónico del usuario
        verify_account.email_verified = True
        verify_account.verifed_at = timezone.now()
        verify_account.save()
        
        # Crea el mensaje de bienvenidad
        subject = 'Welcome to Our Service'
        message = f'Hello {user.username},\n\nThank you for registering with our service.'
        recipient_list = [user.email]

        # Envia el mensaje al correo electrónico del usuario
        email_notification = EmailNotification(subject, message, recipient_list)
        email_notification.send()
        
        # Respuesta de verificación del correo electrónico exitosa
        return Response({
            'status': 'success',
            'message': 'Email verified successfully.'
        }, status=status.HTTP_200_OK)
    
    # No se encuentra al usuario
    except User.DoesNotExist:
        # Respuesta de error al no encontrar el usuario
        return Response({
            'status': 'error',
            'message': 'User not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # No se encuetra el registro de verificación
    except VerifyAccount.DoesNotExist:
        # Respuesta de error al no encontrar el registro de verificación
        return Response({
            'status': 'error',
            'message': 'Verification account not found.'
        }, status=status.HTTP_404_NOT_FOUND)


# Endpoint para el inicio de sesión de usuario
@api_view(['POST'])
def sign_in(request):
    # Obtiene los datos del usuario
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        # Busca al usuario que intenta iniciar sesión
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Respuesta de error al no encontrar el usuario
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
        # Respuesta de error por contraseña incorrecta
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

    # Respuesta de inicio de sesión exitoso
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


# Endpoint para el cierre de sesión de usuario
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sign_out(request):
    # Elimina el token del usuario autenticado
    request.user.auth_token.delete()
    
    # Respuesta de cierre de sesión exitoso
    return Response({
        'status': 'success',
        'message': 'User logged out successfully.'
    }, status=status.HTTP_200_OK)


# Endpoint para actualizar el usuario
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    # Obtiene el usuario autenticado
    user = request.user
    
    # Serializa los datos
    user_update_serializer = UserUpdateSerializer(user, data=request.data, partial=True)

    # Obtiene la validación del serializer
    validation_error = validate_serializer(user_update_serializer)

    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)
    
    # Guarda los cambios del usuario
    user = user_update_serializer.save()

    # Desactiva la cuenta del usuario hasta su verificación
    user.is_active = False
    user.save()

    # Crea o obtiene el registro de verificación del usuario
    verify_account, created = VerifyAccount.objects.get_or_create(user=user)

    # Reinicia el estado de verificación del correo electrónico del usuario
    verify_account.email_verified = False
    verify_account.save()

    # Crea un token para la verifiación del correo electrónico
    token_email = generate_verification_token(user.email)

    # Crea la URL para la verificación del correo electrónico
    verification_url = f'{settings.FRONTEND_URL}/api/users/verify/{token_email}'

    # Crea el mensaje de verificación del correo electrónico
    subject = 'Verify your account'
    message = f'Hello {user.username},\n\nPlease click the link to verify your account: {verification_url}'
    recipient_list = [user.email]

    # Envia el mensaje al correo electrónico del usuario
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

    # Respuesta de actualización de usuario exitoso
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


# Endpoint para eliminar el usuario
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
    try:
        # Elimina el token del usuario autenticado
        request.user.auth_token.delete()

        # Elimina el usuario autenticado
        request.user.delete()

        # Respuesta de eliminación exitoso
        return Response({
            'status': 'success',
            'message': 'User deleted successfully.'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        # Respuesta de error al eliminar el usuario
        return Response({
            'status': 'error',
            'message': 'Error deleting user.',
            'errors': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
