# Generated by Django 2.2.6 on 2019-11-03 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('1', 'admin'), ('2', 'teacher'), ('3', 'leader'), ('4', 'student')], default=4, max_length=5),
        ),
    ]
