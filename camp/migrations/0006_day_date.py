# Generated by Django 2.2.6 on 2019-12-04 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0005_auto_20191204_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='date',
            field=models.DateTimeField(default='2007-10-10 10:10:10'),
        ),
    ]