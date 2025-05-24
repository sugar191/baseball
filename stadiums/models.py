from django.db import models


# Create your models here.
class Stadium(models.Model):
    name = models.CharField(max_length=50)
    sort_order = models.IntegerField(default=0)  # 表示順

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "stadiums"  # 使用するテーブル名を指定
        ordering = ["sort_order"]  # リーグごと、シーズン順位でソート
