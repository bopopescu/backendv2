# Generated by Django 2.2.6 on 2019-11-03 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0002_user_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='description',
            new_name='profile',
        ),
    ]