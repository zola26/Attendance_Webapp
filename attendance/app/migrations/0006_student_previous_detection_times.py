# Generated by Django 4.2.7 on 2024-01-31 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_student_attendance_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='previous_detection_times',
            field=models.JSONField(default=list),
        ),
    ]
