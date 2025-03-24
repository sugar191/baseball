# Generated by Django 5.1.7 on 2025-03-24 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_alter_player_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
