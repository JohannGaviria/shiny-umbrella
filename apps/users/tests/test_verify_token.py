from django.conf import settings
from users.utils import generate_verification_token, confirm_verification_token
from itsdangerous import URLSafeTimedSerializer
import unittest


# Tests para la verificación del token
class VerifyTokenTestCase(unittest.TestCase):
    def setUp(self):
        self.email = "test@example.com"
        self.token = generate_verification_token(self.email)


    def test_generate_verification_token(self):
        """
        Prueba de generar token de verificación.
        """
        self.assertIsNotNone(self.token)
        self.assertIsInstance(self.token, str)


    def test_confirm_verification_token_valid(self):
        """
        Prueba de confirmar token de verificación válido.
        """
        email = confirm_verification_token(self.token)
        self.assertEqual(email, self.email)


    def test_confirm_verification_token_expired(self):
        """
        Prueba de confirmar token de verificación expirado.
        """
        valid_token = generate_verification_token(self.email)
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
        with self.assertRaises(Exception):
            serializer.loads(valid_token, salt=settings.SECURITY_PASSWORD_SALT, max_age=-1)


    def test_confirm_verification_token_invalid(self):
        """
        Prueba de confirmar token de verificación inválido.
        """
        invalid_token = "this_is_an_invalid_token"
        self.assertFalse(confirm_verification_token(invalid_token))


if __name__ == '__main__':
    unittest.main()
