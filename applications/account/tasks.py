from config.celery import app
from decouple import config
from django.core.mail import send_mail


@app.task
def send_user_activation_link(email, activation_code):
    full_link = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    send_mail(
        'from music_service "Yonko"',
        f'Your activation link {full_link}',
        config('EMAIL_HOST_USER'),
        [email]
    )
