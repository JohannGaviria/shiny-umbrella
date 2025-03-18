from django.core.mail import send_mail
from django.conf import settings


class EmailNotification:
    """
    Clase para enviar notificaciones por correo electrónico.

    Args:
        subject (str): Asunto del correo electrónico.
        message (str): Mensaje del correo electrónico.
        recipient_list (list): Lista de destinatarios del correo electrónico.
    """
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        self.sender = settings.EMAIL_HOST_USER


    def send(self, fail_silently=False):
        """
        Envía el mensaje al correo electrónico usando los parámetros proporcionados.

        Args:
            fail_silently (bool): Si se establece en True, suprime las excepciones en caso de error.
        """
        send_mail(
            self.subject,
            self.message,
            self.sender,
            self.recipient_list,
            fail_silently=fail_silently,
        )
