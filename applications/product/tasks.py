from decouple import config
from django.core.mail import send_mail

from applications.product.models import Music
from config.celery import app


@app.task
def send_paid_confirm(email):
    full_link = f'http://localhost:8000/api/v1/product/post_confirm/{"id вашей музыки"}'
    send_mail(
        'From music service "Yonko"',
        f'To confirm the process go by link : {full_link}',
        config('EMAIL_HOST_USER'),
        [email]
    )


@app.task
def delete_not_paid_music():
    musics = Music.objects.delete(is_paid=False)
    musics.delete()
    musics.save()
