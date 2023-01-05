import logging

from django.contrib.auth import get_user_model

from applications.account.parser import get_url
from config.celery import app
from decouple import config
from django.core.mail import send_mail

User = get_user_model()
URL = 'https://lenta.ru/rubrics/culture/music/'
logger = logging.getLogger('celery_logger')


@app.task
def send_user_activation_link(email, activation_code):
    logger.info('send_activation_link')
    full_link = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    send_mail(
        'from music_service "Yonko"',
        f'Your activation link {full_link}',
        config('EMAIL_HOST_USER'),
        [email]
    )


@app.task
def send_user_forgot_password_code(email, activation_code):
    logger.info('send_user_forgot_password_code')
    send_mail(
        'from music_service "Yonko"',
        f'Your link to change password {activation_code}',
        config('EMAIL_HOST_USER'),
        [email]
    )


email_list = [queryset.email for queryset in User.objects.filter(is_subscribed=True)]


@app.task
def send_spam():
    logger.info('send_spam')
    send_mail(
        'from music service "Yonko"',
        f'{get_url(URL)}',
        config('EMAIL_HOST_USER'),
        email_list
    )
