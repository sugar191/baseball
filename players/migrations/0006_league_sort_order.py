# Generated by Django 5.1.7 on 2025-03-24 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_alter_league_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='sort_order',
            field=models.IntegerField(default=0),
        ),
    ]
