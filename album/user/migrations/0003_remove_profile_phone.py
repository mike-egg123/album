# Generated by Django 2.2 on 2021-06-29 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profile_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone',
        ),
    ]
