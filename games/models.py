from django.db import models
from teams.models import TeamSeason
from stadiums.models import Stadium


class GameStatus(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = "game_status"  # 使用するテーブル名を指定

    def __str__(self):
        return self.name


# Create your models here.
class Game(models.Model):
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    home_team = models.ForeignKey(
        TeamSeason,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="home_games",
    )
    away_team = models.ForeignKey(
        TeamSeason,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="away_games",
    )
    game_status = models.ForeignKey(
        GameStatus, on_delete=models.RESTRICT, null=True, blank=True
    )
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    stadium = models.ForeignKey(
        Stadium, on_delete=models.RESTRICT, null=True, blank=True
    )
    remarks = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.date}"

    class Meta:
        db_table = "games"  # 使用するテーブル名を指定
