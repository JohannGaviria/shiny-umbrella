from django.conf import settings
from .utils import EmailNotification
from unittest.mock import patch
import unittest


# Tests para las notificaciones del correo electrónico
class EmailNotificationTestCase(unittest.TestCase):
    def setUp(self):
        self.subject = "Test Subject"
        self.message = "This is a test message."
        self.recipient_list = ["recipient@example.com"]
        self.notification = EmailNotification(self.subject, self.message, self.recipient_list)


    @patch('apps.notification.utils.send_mail')
    def test_send_email_successful(self, mock_send_mail):
        """
        Prueba de enviar correo electrónico correctamente.
        """
        self.notification.send()
        mock_send_mail.assert_called_once_with(
            self.subject,
            self.message,
            settings.EMAIL_HOST_USER,
            self.recipient_list,
            fail_silently=False,
        )


    @patch('apps.notification.utils.send_mail')
    def test_send_email_fail_silently(self, mock_send_mail):
        """
        Prueba de enviar correo electrónico cuando fail_silently es True.
        """
        self.notification.send(fail_silently=True)
        mock_send_mail.assert_called_once_with(
            self.subject,
            self.message,
            settings.EMAIL_HOST_USER,
            self.recipient_list,
            fail_silently=True,
        )


if __name__ == '__main__':
    unittest.main()
