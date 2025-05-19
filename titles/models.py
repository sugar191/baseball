from django.db import models
from players.models import Player
from positions.models import Position
from seasons.models import Season

# Create your models here.


# タイトル
class Title(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # 名前
    sort_order = models.IntegerField(default=0)  # 表示順

    class Meta:
        db_table = "titles"  # 使用するテーブル名を指定

    def __str__(self):
        return self.name


# 選手タイトル
class PlayerTitle(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.IntegerField()  # 年度（シーズン）
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, null=True, blank=True
    )  # シーズン
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "player_titles"  # 使用するテーブル名を指定

    def __str__(self):
        return f"{self.player.name}"


# 検索ビュー
class PlayerLatestTitleView(models.Model):
    id = models.IntegerField(primary_key=True)
    team_id = models.IntegerField(null=True, blank=True)
    title_id = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    player_id = models.IntegerField(null=True, blank=True)
    player_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        managed = False  # DjangoがCREATE TABLEしないように
        db_table = "player_latest_title_view"

    def __str__(self):
        return f"{self.team_id}"


# 検索ビュー
class PlayerTitleView(models.Model):
    id = models.IntegerField(primary_key=True)
    title_id = models.IntegerField(null=True, blank=True)
    position_id = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    season_label = models.CharField(max_length=50, null=True, blank=True)
    team_logo = models.ImageField(upload_to="team_logos/", null=True, blank=True)
    player_id = models.IntegerField(null=True, blank=True)
    player_name = models.CharField(max_length=50, null=True, blank=True)
    batting_average = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, blank=True
    )  # 打率
    home_runs = models.IntegerField(null=True, blank=True)  # 本塁打
    runs_batted_in = models.IntegerField(null=True, blank=True)  # 打点
    stolen_bases = models.IntegerField(null=True, blank=True)  # 盗塁
    on_base_percentage = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, blank=True
    )  # 出塁率
    hits = models.IntegerField(null=True, blank=True)  # 安打
    wins = models.IntegerField(null=True, blank=True)  # 勝利
    earned_run_average = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # 防御率
    win_average = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # 勝率
    strike_outs = models.IntegerField(null=True, blank=True)  # 奪三振
    saves = models.IntegerField(null=True, blank=True)  # セーブ
    holds = models.IntegerField(null=True, blank=True)  # ホールド

    class Meta:
        managed = False  # DjangoがCREATE TABLEしないように
        db_table = "player_title_view"

    def __str__(self):
        return f"{self.player_name}"
