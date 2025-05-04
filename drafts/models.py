from django.db import models
from players.models import Player
from positions.models import PositionCategory
from teams.models import Team

# Create your models here.

# ドラフト種別
class DraftCategory(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # 名前
    sort_order = models.IntegerField(default=0)  # 表示順

    class Meta:
        db_table = 'draft_categories'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# ドラフト
class Draft(models.Model):
    year = models.IntegerField()  # 年度（シーズン）
    draft_category = models.ForeignKey(DraftCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'drafts'  # 使用するテーブル名を指定

    def __str__(self):
        return f"{self.year}"

# 選手ドラフト
class PlayerDraft(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # 所属球団
    rank = models.IntegerField()
    position_category = models.ForeignKey(PositionCategory, on_delete=models.RESTRICT, null=True, blank=True)
    is_reverse_nomination = models.BooleanField(null=True, blank=True)
    is_hit = models.BooleanField(null=True, blank=True)
    miss_count = models.IntegerField()
    is_joined = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'player_drafts'  # 使用するテーブル名を指定

    def __str__(self):
        return f"{self.player.name} ({self.draft})"
