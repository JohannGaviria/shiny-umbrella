from .models import Survey, Invitation


def get_survey_by_id(survey_id):
    """
    Función para obtener una encuesta por su ID.

    Args:
        survey_id (int): ID de la encuesta a obtener.

    Returns:
        Survey: Objeto Survey si se encuentra.
        dict: Diccionario con el estado de error y el mensaje si no se encuentra.
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


def check_survey_is_public(survey):
    """
    Función para verificar si la encuesta es pública o privada.

    Args:
        survey (Survey): Objeto Survey a verificar.

    Returns:
        bool: True si la encuesta es pública, False si es privada.
    """
    return survey.is_public


def check_user_invited(survey, request_user_email):
    """
    Función para comprobar si un usuario está invitado a una encuesta.

    Args:
        survey (Survey): Objeto Survey a verificar.
        request_user_email (str): Correo electrónico del usuario a verificar.

    Returns:
        dict: Diccionario con el estado de error y el mensaje si el usuario no está invitado.
        None: Si el usuario está invitado.
    """
    # Verifica que el usuario este invitado a responder la encuesta
    if not Invitation.objects.filter(survey=survey, email=request_user_email).first():
        # Respuesta erronea al usuario no tener permiso
        return {
            'status': 'error',
            'message': 'You do not have permission to interact with this survey.'
        }
    return None
