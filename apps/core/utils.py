from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


class CustomPageNumberPagination(PageNumberPagination):
    """
    Clase personalizada para la paginación de los endpoints.

    Atributos:
        page_size_query_param (str): Nombre del parámetro de consulta para el tamaño de la página.
        max_page_size (int): Tamaño máximo de la página.
    """
    page_size_query_param = 'page_size'
    max_page_size = 100


    def get_paginated_response(self, data):
        """
        Genera una respuesta paginada con los datos proporcionados.

        Args:
            data (list): Lista de datos a paginar.

        Returns:
            Response: Respuesta paginada con los datos.
        """
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })


def validate_serializer(serializer):
    """
    Función para comprobar la validación del serializador.

    Args:
        serializer (Serializer): Serializador a validar.

    Returns:
        dict: Diccionario con el estado de la validación y los errores, si los hay.
    """
    # Verifica los datos del serialzer
    if not serializer.is_valid():
        # Respuesta de error en la validación del serializer
        return {
            'status': 'error',
            'message': 'Errors in data validation.',
            'errors': serializer.errors
        }
    return None


def verify_user_is_creator(element, request_user, message):
    """
    Verifica que el usuario sea el creador del elemento.

    Args:
        element (Model): Elemento a verificar.
        request_user (User): Usuario que realiza la solicitud.
        message (str): Mensaje de error en caso de que el usuario no sea el creador.

    Returns:
        dict: Diccionario con el estado de la verificación y el mensaje de error, si lo hay.
    """
    # Verifica que el usuario no sea creador
    if element.user != request_user:
        # Respuesta erronea al usuario no ser el creador
        return {
            'status': 'error',
            'message': message
        }
    return None
