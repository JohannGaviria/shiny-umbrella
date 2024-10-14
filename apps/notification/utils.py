from django.core.mail import send_mail
from django.conf import settings


# Clase para las notificaciones de la API
class EmailNotification:
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        self.sender = settings.EMAIL_HOST_USER

    def send(self, fail_silently=False):
        """
        Envía el correo electrónico usando los parámetros proporcionados.
        """
        send_mail(
            self.subject,
            self.message,
            self.sender,
            self.recipient_list,
            fail_silently=fail_silently,
        )
