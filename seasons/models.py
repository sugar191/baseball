from django.db import models


# Create your models here.
class Season(models.Model):
    year = models.IntegerField(null=True, blank=True)
    label = models.CharField(max_length=50, null=True, blank=True)
    organization = models.ForeignKey(
        "teams.Organization", on_delete=models.CASCADE, null=True, blank=True
    )  # リーグとの関連
    sort_order = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "seasons"  # 使用するテーブル名を指定

    def __str__(self):
        return f"{self.year}{self.label}({self.organization})"
