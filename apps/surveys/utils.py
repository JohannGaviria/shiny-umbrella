from .models import Survey


def get_survey_by_id(survey_id):
    """
    Función para obtener una encuesta por su ID.
    """
    try:
        # Obtiene la encuesta mediante su ID
        return Survey.objects.get(id=survey_id)
    except Survey.DoesNotExist:
        # Respuesta erronea a no encontrar la encuesta
        return {
            'status': 'error',
            'message': 'Survey not found.'
        }
    