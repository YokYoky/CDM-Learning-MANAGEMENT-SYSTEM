# Generated by Django 5.0.4 on 2024-05-11 10:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_remove_course_professor'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='coursesEnrolled',
        ),
        migrations.AddField(
            model_name='student',
            name='coursesEnrolled',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course'),
        ),
    ]
