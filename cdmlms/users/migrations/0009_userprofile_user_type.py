# Generated by Django 5.0.4 on 2024-05-14 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_userprofile_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[(1, 'Staff'), (2, 'Student')], default=1, max_length=1),
        ),
    ]
