from django.db import models

# 出身地テーブル
class Place(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # 場所名
    sort_order = models.IntegerField(default=0)  # 表示順
    is_foreign = models.BooleanField(default=True)  #海外かどうか

    class Meta:
        db_table = 'places'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name