# Generated by Django 5.1.2 on 2024-10-31 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersession',
            name='user_id',
        ),
    ]
