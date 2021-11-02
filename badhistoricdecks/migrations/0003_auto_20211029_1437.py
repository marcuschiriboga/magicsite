# Generated by Django 3.2.8 on 2021-10-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardhandler', '0003_card_rarity'),
        ('badhistoricdecks', '0002_alter_deck_format'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='card_highlights',
            field=models.ManyToManyField(blank=True, related_name='card_highlights', to='cardhandler.Card'),
        ),
        migrations.AlterField(
            model_name='deck',
            name='card_obj_in_deck',
            field=models.ManyToManyField(blank=True, related_name='card_obj_in_deck', to='cardhandler.Card'),
        ),
    ]
