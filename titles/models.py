from django.db import models
from players.models import Player
from positions.models import Position

# Create your models here.

# タイトル
class Title(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # 名前
    sort_order = models.IntegerField(default=0)  # 表示順

    class Meta:
        db_table = 'titles'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# 選手タイトル
class PlayerTitle(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.IntegerField()  # 年度（シーズン）
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'player_titles'  # 使用するテーブル名を指定

    def __str__(self):
        return f"{self.player.name}"