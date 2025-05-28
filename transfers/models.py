from django.db import models
from players.models import Player
from teams.models import TeamSeason


# Create your models here.
class TransferType(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = "transfer_types"  # 使用するテーブル名を指定

    def __str__(self):
        return self.name


class Transfer(models.Model):
    date = models.DateField(null=True, blank=True)
    transfer_type = models.ForeignKey(
        TransferType, on_delete=models.RESTRICT, null=True, blank=True
    )

    class Meta:
        db_table = "transfers"  # 使用するテーブル名を指定

    def __str__(self):
        return f"{self.date}{self.transfer_type}"


class PlayerTransfer(models.Model):
    transfer = models.ForeignKey(
        Transfer, on_delete=models.RESTRICT, null=True, blank=True
    )
    player = models.ForeignKey(Player, on_delete=models.RESTRICT, null=True, blank=True)
    from_team = models.ForeignKey(
        TeamSeason,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="transfers_from",
    )
    to_team = models.ForeignKey(
        TeamSeason,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="transfers_to",
    )

    class Meta:
        db_table = "player_transfers"  # 使用するテーブル名を指定

    def __str__(self):
        return self.transfer
