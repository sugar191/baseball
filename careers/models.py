from django.db import models
from places.models import Place
from players.models import Player


# Create your models here.
# 経歴カテゴリ
class CareerCategory(models.Model):
    name = models.CharField(max_length=10)
    label = models.CharField(max_length=10, null=True, blank=True)
    sort_order = models.IntegerField()

    class Meta:
        db_table = "career_categories"  # 使用するテーブル名を指定

    def __str__(self):
        return self.name


# 経歴
class Career(models.Model):
    name = models.CharField(max_length=50)
    career_category = models.ForeignKey(
        CareerCategory, on_delete=models.RESTRICT, null=True, blank=True
    )
    is_private = models.BooleanField(null=True)
    place = models.ForeignKey(Place, on_delete=models.RESTRICT, null=True, blank=True)
    wikipedia_parameter1 = models.CharField(
        max_length=500, null=True, blank=True
    )  #  WikipediaURLパラメータ
    wikipedia_parameter2 = models.CharField(
        max_length=500, null=True, blank=True
    )  #  WikipediaURLパラメータ

    class Meta:
        db_table = "careers"  # 使用するテーブル名を指定

    def __str__(self):
        return self.name


# 経歴バージョン
class CareerVersion(models.Model):
    name = models.CharField(max_length=50)
    career = models.ForeignKey(Career, on_delete=models.RESTRICT, null=True, blank=True)
    version = models.IntegerField(default=0)

    class Meta:
        db_table = "career_versions"  # 使用するテーブル名を指定

    def __str__(self):
        return self.name


# 経歴
class PlayerCareer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    career_version = models.ForeignKey(
        CareerVersion, on_delete=models.RESTRICT, null=True, blank=True
    )
    sort_order = models.IntegerField()
    remarks = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "player_careers"  # 使用するテーブル名を指定
        indexes = [
            models.Index(fields=["player", "sort_order"]),
        ]

    def __str__(self):
        return f"{self.player.name} ({self.career_version.name})"


class PlayerCareerView(models.Model):
    player_career_id = models.IntegerField(primary_key=True)
    career_id = models.IntegerField()
    player_id = models.IntegerField()
    player_name = models.CharField(max_length=50, null=False, blank=False)
    player_furigana = models.CharField(max_length=50, null=True, blank=True)
    player_birthday = models.DateField(null=True, blank=True)
    after_career_id = models.IntegerField()
    after_career_name = models.CharField(max_length=50)
    draft_year = models.IntegerField()
    team_logo = models.ImageField(upload_to="team_logos/", null=True, blank=True)
    draft_category_name = models.CharField(max_length=50, null=False, blank=False)
    player_draft_rank = models.IntegerField()
    player_draft_miss_count = models.IntegerField()

    class Meta:
        managed = False  # Djangoにマイグレーションさせない
        db_table = "player_careers_view"
