from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


# Clase para la paginación de los endpoints
class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100


    def get_paginated_response(self, data):
        """
        Respuesta de los datos al hacer paginación.
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
