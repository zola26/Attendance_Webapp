# Generated by Django 4.2.7 on 2023-12-31 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('major', models.CharField(max_length=100)),
                ('starting_year', models.IntegerField()),
                ('total_attendance', models.IntegerField()),
                ('standing', models.CharField(max_length=1)),
                ('year', models.IntegerField()),
                ('last_attendance_time', models.DateTimeField()),
            ],
        ),
    ]
