# Generated by Django 5.0.4 on 2024-05-11 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='professor',
        ),
    ]
