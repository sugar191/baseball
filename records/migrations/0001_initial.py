# Generated by Django 5.1.7 on 2025-05-04 08:43

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('players', '0001_initial'),
        ('positions', '0001_initial'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('symbol', models.CharField(default='', max_length=10)),
            ],
            options={
                'db_table': 'currencies',
            },
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='records.currency')),
            ],
            options={
                'db_table': 'exchange_rates',
                'unique_together': {('year', 'currency')},
            },
        ),
        migrations.CreateModel(
            name='PlayerBattingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('games', models.IntegerField(blank=True, null=True)),
                ('plate_appearances', models.IntegerField(blank=True, null=True)),
                ('at_bats', models.IntegerField(blank=True, null=True)),
                ('runs', models.IntegerField(blank=True, null=True)),
                ('hits', models.IntegerField(blank=True, null=True)),
                ('doubles', models.IntegerField(blank=True, null=True)),
                ('triples', models.IntegerField(blank=True, null=True)),
                ('home_runs', models.IntegerField(blank=True, null=True)),
                ('total_bases', models.IntegerField(blank=True, null=True)),
                ('runs_batted_in', models.IntegerField(blank=True, null=True)),
                ('stolen_bases', models.IntegerField(blank=True, null=True)),
                ('caught_stealing', models.IntegerField(blank=True, null=True)),
                ('sacrifice_bunts', models.IntegerField(blank=True, null=True)),
                ('sacrifice_flys', models.IntegerField(blank=True, null=True)),
                ('bases_on_balls', models.IntegerField(blank=True, null=True)),
                ('intentional_walks', models.IntegerField(blank=True, null=True)),
                ('hit_by_pitch', models.IntegerField(blank=True, null=True)),
                ('strike_outs', models.IntegerField(blank=True, null=True)),
                ('grounded_into_double_plays', models.IntegerField(blank=True, null=True)),
                ('interferences', models.IntegerField(blank=True, null=True)),
                ('batting_average', models.DecimalField(blank=True, decimal_places=3, max_digits=4, null=True)),
                ('on_base_percentage', models.DecimalField(blank=True, decimal_places=3, max_digits=4, null=True)),
                ('slugging_percentage', models.DecimalField(blank=True, decimal_places=3, max_digits=4, null=True)),
                ('ops', models.DecimalField(blank=True, decimal_places=3, max_digits=4, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.player')),
            ],
            options={
                'db_table': 'player_batting_records',
                'unique_together': {('player', 'year')},
            },
        ),
        migrations.CreateModel(
            name='PlayerCommonRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('number', models.CharField(blank=True, max_length=5, null=True)),
                ('registered_name', models.CharField(blank=True, max_length=50, null=True)),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='records.currency')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team')),
            ],
            options={
                'db_table': 'player_common_records',
                'ordering': ['year'],
                'unique_together': {('player', 'year')},
            },
        ),
        migrations.CreateModel(
            name='PlayerFieldingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('games', models.IntegerField(blank=True, null=True)),
                ('put_outs', models.IntegerField(blank=True, null=True)),
                ('assists', models.IntegerField(blank=True, null=True)),
                ('errors', models.IntegerField(blank=True, null=True)),
                ('double_plays', models.IntegerField(blank=True, null=True)),
                ('fielding_percentage', models.DecimalField(blank=True, decimal_places=3, max_digits=4, null=True)),
                ('passed_balls', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.player')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='positions.position')),
            ],
            options={
                'db_table': 'player_fielding_records',
                'unique_together': {('player', 'year', 'position')},
            },
        ),
        migrations.CreateModel(
            name='PlayerPitchingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('games', models.IntegerField(blank=True, null=True)),
                ('games_started', models.IntegerField(blank=True, null=True)),
                ('games_finished', models.IntegerField(blank=True, null=True)),
                ('complete_games', models.IntegerField(blank=True, null=True)),
                ('shutouts', models.IntegerField(blank=True, null=True)),
                ('no_base_on_balls_games', models.IntegerField(blank=True, null=True)),
                ('wins', models.IntegerField(blank=True, null=True)),
                ('loses', models.IntegerField(blank=True, null=True)),
                ('saves', models.IntegerField(blank=True, null=True)),
                ('holds', models.IntegerField(blank=True, null=True)),
                ('innings_pitched', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('plate_appearances', models.IntegerField(blank=True, null=True)),
                ('at_bats', models.IntegerField(blank=True, null=True)),
                ('hits', models.IntegerField(blank=True, null=True)),
                ('home_runs', models.IntegerField(blank=True, null=True)),
                ('walks', models.IntegerField(blank=True, null=True)),
                ('hit_batsmen', models.IntegerField(blank=True, null=True)),
                ('strike_outs', models.IntegerField(blank=True, null=True)),
                ('wild_pitches', models.IntegerField(blank=True, null=True)),
                ('balk', models.IntegerField(blank=True, null=True)),
                ('runs', models.IntegerField(blank=True, null=True)),
                ('earned_runs', models.IntegerField(blank=True, null=True)),
                ('earned_run_average', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('whip', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.player')),
            ],
            options={
                'db_table': 'player_pitching_records',
                'unique_together': {('player', 'year')},
            },
        ),
    ]
