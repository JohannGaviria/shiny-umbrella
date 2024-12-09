from .models import Comment, Qualify


def get_comment_by_id(comment_id):
    """
    Función para obtener una encuesta por su ID.
    """
    try:
        # Busca el comentario de la encuesta por su ID
        return Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        # Respuesta erronea al no encontrar el comentario
        return {
            'status': 'error',
            'message': 'Comment not found.'
        }


def get_qualify_by_id(qualify_id):
    """
    Función para obtener una calificación por su ID.
    """
    try:
        return Qualify.objects.get(id=qualify_id)
    except Qualify.DoesNotExist:
        # Respuesta erronea al no encontrar la calificación
        return {
            'status': 'error',
            'message': 'Qualify not found.'
        }