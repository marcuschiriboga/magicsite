# Generated by Django 3.2.8 on 2021-10-22 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardhandler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='layout',
            field=models.CharField(max_length=40),
        ),
    ]
