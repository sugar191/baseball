from django.db import models

# ポジション種別
class PositionCategory(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # 名前
    sort_order = models.IntegerField(default=0)  # 表示順

    class Meta:
        db_table = 'position_categories'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# ポジション
class Position(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # 名前
    position_category = models.ForeignKey(PositionCategory, on_delete=models.CASCADE, null=True, blank=True)
    sort_order = models.IntegerField(default=0)  # 表示順

    class Meta:
        db_table = 'positions'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name