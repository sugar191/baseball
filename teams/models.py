from django.db import models
from django.utils import timezone

# Create your models here.
# 組織テーブル
class Organization(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'organizations'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# リーグテーブル
class League(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False)
    sort_order = models.IntegerField(default=0)  # 表示順を決めるフィールド
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)  # リーグとの関連

    class Meta:
        db_table = 'leagues'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# 球団テーブル
class Team(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)  # 球団ロゴ画像
    league = models.ForeignKey(League, on_delete=models.CASCADE)  # リーグとの関連
    sort_order = models.IntegerField(default=0)  # 表示順（順位に基づく）
    color = models.CharField(max_length=50, null=True, blank=True) # 球団カラーのカラーコード
    is_select = models.BooleanField(null=True)
    usukoi_parameter = models.CharField("日本プロ野球記録", max_length=50, null=True, blank=True)  # 日本プロ野球記録サイトのパラメータ
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'teams'  # 使用するテーブル名を指定
        ordering = ['league', 'sort_order']  # リーグごと、シーズン順位でソート
        indexes = [
            models.Index(fields=['league']),
        ]
