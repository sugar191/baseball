# Generated by Django 5.1.7 on 2025-05-14 07:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seasons', '0002_season_label_season_organization'),
        ('titles', '0002_playerlatesttitleview'),
    ]

    operations = [
        migrations.AddField(
            model_name='playertitle',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='seasons.season'),
        ),
    ]
