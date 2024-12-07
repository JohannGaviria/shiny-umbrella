from rest_framework.authtoken.models import Token
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.surveys.models import Survey, Option, Ask, Answer
from apps.feedback.models import Comment, Qualify
from faker import Faker
import random
from django.utils import timezone

fake = Faker()

class Command(BaseCommand):
    help = 'Create data for analysis including a survey and 10 users to answer it.'

    def handle(self, *args, **options):
        self.stdout.write('Creating data for analysis...')

        # 1. Crear un usuario creador de la encuesta
        user_create = User.objects.create(username=fake.user_name(), email=fake.email(), is_active=True)
        user_create.set_password(fake.password())
        user_create.save()
        Token.objects.create(user=user_create)

        # 2. Crear una encuesta
        survey = Survey.objects.create(
            title=fake.sentence(),
            description=fake.text(),
            start_date=timezone.now(),
            end_date=timezone.now(),
            is_public=True,
            user=user_create,
        )

        # 3. Crear preguntas de la encuesta
        question_1 = Ask.objects.create(
            text='What is your favorite programming language?',
            type='multiple',
            survey=survey
        )
        question_2 = Ask.objects.create(
            text='Do you like Django?',
            type='boolean',
            survey=survey
        )
        question_3 = Ask.objects.create(
            text='How long have you been programming?',
            type='short',
            survey=survey
        )
        question_4 = Ask.objects.create(
            text='What is your opinion on JavaScript?',
            type='short',
            survey=survey
        )
        question_5 = Ask.objects.create(
            text='Have you worked with databases?',
            type='boolean',
            survey=survey
        )
        question_6 = Ask.objects.create(
            text='What is your experience with machine learning?',
            type='multiple',
            survey=survey
        )
        question_7 = Ask.objects.create(
            text='Do you prefer backend over frontend development?',
            type='boolean',
            survey=survey
        )

        # 4. Crear opciones para la primera y sexta pregunta (opciones múltiples)
        option_1_q1 = Option.objects.create(text='Python', ask=question_1)
        option_2_q1 = Option.objects.create(text='JavaScript', ask=question_1)
        option_3_q1 = Option.objects.create(text='Java', ask=question_1)

        option_1_q6 = Option.objects.create(text='No experience', ask=question_6)
        option_2_q6 = Option.objects.create(text='Basic experience', ask=question_6)
        option_3_q6 = Option.objects.create(text='Advanced experience', ask=question_6)

        # 5. Crear 10 usuarios para responder la encuesta
        users = []
        for _ in range(10):
            user = User.objects.create(username=fake.user_name(), email=fake.email(), is_active=True)
            user.set_password(fake.password())
            user.save()
            Token.objects.create(user=user)
            users.append(user)

        # 6. Crear respuestas de los usuarios para la encuesta
        for user in users:
            # Responder a la primera pregunta (opciones múltiples)
            selected_option_q1 = random.choice([option_1_q1, option_2_q1, option_3_q1])
            Answer.objects.create(
                content_answer=None,
                user=user,
                ask=question_1,
                option=selected_option_q1
            )

            # Responder a la segunda pregunta (booleano)
            answer_boolean_q2 = random.choice([True, False])
            Answer.objects.create(
                content_answer=str(answer_boolean_q2),
                user=user,
                ask=question_2,
                option=None
            )

            # Responder a la tercera pregunta (respuesta corta)
            answer_short_q3 = fake.text(max_nb_chars=100)
            Answer.objects.create(
                content_answer=answer_short_q3,
                user=user,
                ask=question_3,
                option=None
            )

            # Responder a la cuarta pregunta (respuesta corta)
            answer_short_q4 = fake.text(max_nb_chars=100)
            Answer.objects.create(
                content_answer=answer_short_q4,
                user=user,
                ask=question_4,
                option=None
            )

            # Responder a la quinta pregunta (booleano)
            answer_boolean_q5 = random.choice([True, False])
            Answer.objects.create(
                content_answer=str(answer_boolean_q5),
                user=user,
                ask=question_5,
                option=None
            )

            # Responder a la sexta pregunta (opciones múltiples)
            selected_option_q6 = random.choice([option_1_q6, option_2_q6, option_3_q6])
            Answer.objects.create(
                content_answer=None,
                user=user,
                ask=question_6,
                option=selected_option_q6
            )

            # Responder a la séptima pregunta (booleano)
            answer_boolean_q7 = random.choice([True, False])
            Answer.objects.create(
                content_answer=str(answer_boolean_q7),
                user=user,
                ask=question_7,
                option=None
            )

        # 7. Crear un comentario y una calificación para la encuesta
        for user in users:
            Comment.objects.create(
                content=fake.text(),
                user=user,
                survey=survey
            )

            Qualify.objects.create(
                assessment=random.randint(1, 5),
                user=user,
                survey=survey
            )

        self.stdout.write(self.style.SUCCESS('Data created successfully!'))
