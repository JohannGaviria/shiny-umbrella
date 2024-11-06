from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


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
