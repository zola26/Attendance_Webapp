# Generated by Django 4.2.7 on 2024-01-19 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.ImageField(default=str, upload_to='images/'),
            preserve_default=False,
        ),
    ]