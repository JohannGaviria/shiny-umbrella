from django.conf import settings
from itsdangerous import URLSafeTimedSerializer


def generate_verification_token(email):
    """
    Genera un token para la verificación del email
    """
    # Serializa la clave secreta definida en la configuración
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    # Genera y retorna un token seguro para el email con un salt específico
    return serializer.dumps(email, salt=settings.SECURITY_PASSWORD_SALT)


def confirm_verification_token(token, expiration=3600):
    """
    Confirma el token de verificación del email
    """
    # Serializa la clave secreta definida en la configuración
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        # Carga el email desde el token, verificando que no haya expirado
        email = serializer.loads(token, salt=settings.SECURITY_PASSWORD_SALT, max_age=expiration)
    except:
        # Retorna False si hay un error
        return False
    # Retorna el email asociado
    return email

