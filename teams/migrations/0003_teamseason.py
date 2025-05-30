# Generated by Django 5.1.7 on 2025-05-24 02:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seasons', '0003_season_sort_order'),
        ('stadiums', '0001_initial'),
        ('teams', '0002_alter_league_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='team_logos/')),
                ('sort_order', models.IntegerField(default=0)),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='seasons.season')),
                ('stadium', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stadiums.stadium')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team')),
            ],
            options={
                'db_table': 'team_seasons',
            },
        ),
    ]
