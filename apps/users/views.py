from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Endpoint for user registration
@api_view(['POST'])
def sign_up(request):
    # Respuesta exitosa desde el endpoint
    return Response({
        'status': 'success',
        'message': 'User registered successfully.'
    }, status=status.HTTP_201_CREATED)


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
