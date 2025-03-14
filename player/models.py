from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'players'  # 既存のテーブル名を指定
        managed = False  # Djangoにテーブルを管理させない（既存テーブルを使用するため）

    def __str__(self):
        return self.name