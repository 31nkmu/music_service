# Generated by Django 4.1.4 on 2023-01-03 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favourite',
            name='album',
        ),
    ]