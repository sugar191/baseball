from django.db import models
from django.utils import timezone
from players.models import Player
from positions.models import Position
from teams.models import Team

# 通貨
class Currency(models.Model):
    code = models.CharField(max_length=10, null=False, blank=False, unique=True)  # 通貨コード
    name = models.CharField(max_length=30, null=False, blank=False)  # 通貨
    symbol = models.CharField(max_length=10, null=False, blank=False, default="")  # 通貨記号

    class Meta:
        db_table = 'currencies'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# 円レート
class ExchangeRate(models.Model):
    year = models.IntegerField()  # 年度
    currency = models.ForeignKey(Currency, on_delete=models.RESTRICT, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)  # 1単位あたりの円レート（例: 1 USD = 110円）

    class Meta:
        db_table = 'exchange_rates'  # 使用するテーブル名を指定
        unique_together = ('year', 'currency')  # 同じ年と通貨の組み合わせを一意に

    def __str__(self):
        return f"{self.year} - {self.currency.code if self.currency else '不明'}"

# 選手共通記録
class PlayerCommonRecord(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.IntegerField()  # 年度（シーズン）
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # 所属球団
    number = models.CharField(max_length=5, null=True, blank=True)  # 背番号
    registered_name = models.CharField(max_length=50, null=True, blank=True)  # 登録名
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # 最大12桁、2桁小数点
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)  # 通貨
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'player_common_records'  # 使用するテーブル名を指定
        unique_together = ('player', 'year')  # 選手と年度の組み合わせは一意
        ordering = ['year']  # yearでソート

    def __str__(self):
        return f"{self.player.name} ({self.year})"

    # 年齢を計算するプロパティ
    @property
    def age(self):
        if self.player.birthday:
            return self.year - self.player.birthday.year
        return None

# 選手投手記録
class PlayerPitchingRecord(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.IntegerField()  # 年度（シーズン）
    games = models.IntegerField(null=True, blank=True)  # 登板
    games_started = models.IntegerField(null=True, blank=True)  # 先発
    games_finished = models.IntegerField(null=True, blank=True)  # 完了
    complete_games = models.IntegerField(null=True, blank=True)  # 完投
    shutouts = models.IntegerField(null=True, blank=True)  # 完封
    no_base_on_balls_games = models.IntegerField(null=True, blank=True)  # 無四
    wins = models.IntegerField(null=True, blank=True)  # 勝利
    loses = models.IntegerField(null=True, blank=True)  # 敗戦
    saves = models.IntegerField(null=True, blank=True)  # セーブ
    holds = models.IntegerField(null=True, blank=True)  # ホールド
    innings_pitched = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)  # 投球回
    plate_appearances = models.IntegerField(null=True, blank=True)  # 打者
    at_bats = models.IntegerField(null=True, blank=True)  # 打数
    hits = models.IntegerField(null=True, blank=True)  # 安打
    home_runs = models.IntegerField(null=True, blank=True)  # 本塁
    walks = models.IntegerField(null=True, blank=True)  # 四球
    hit_batsmen = models.IntegerField(null=True, blank=True)  # 死球
    strike_outs = models.IntegerField(null=True, blank=True)  # 奪三振
    wild_pitches = models.IntegerField(null=True, blank=True)  # 暴投
    balk = models.IntegerField(null=True, blank=True)  # ボーク
    runs = models.IntegerField(null=True, blank=True)  # 失点
    earned_runs = models.IntegerField(null=True, blank=True)  # 自責点
    earned_run_average = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 防御率
    whip = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # WHIP
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'player_pitching_records'  # 使用するテーブル名を指定
        unique_together = ('player', 'year')  # 選手と年度の組み合わせは一意

    def __str__(self):
        return f"{self.player.name} ({self.year})"

# 選手打撃記録
class PlayerBattingRecord(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.IntegerField()  # 年度（シーズン）
    games = models.IntegerField(null=True, blank=True)  # 出場試合
    plate_appearances = models.IntegerField(null=True, blank=True)  # 打席
    at_bats = models.IntegerField(null=True, blank=True)  # 打席
    runs = models.IntegerField(null=True, blank=True)  # 得点
    hits = models.IntegerField(null=True, blank=True)  # 安打
    doubles = models.IntegerField(null=True, blank=True)  # 二塁打
    triples = models.IntegerField(null=True, blank=True)  # 三塁打
    home_runs = models.IntegerField(null=True, blank=True)  # 本塁打
    total_bases = models.IntegerField(null=True, blank=True)  # 塁打
    runs_batted_in = models.IntegerField(null=True, blank=True)  # 打点
    stolen_bases = models.IntegerField(null=True, blank=True)  # 盗塁
    caught_stealing = models.IntegerField(null=True, blank=True)  # 盗刺
    sacrifice_bunts = models.IntegerField(null=True, blank=True)  # 犠打
    sacrifice_flys = models.IntegerField(null=True, blank=True)  # 犠飛
    bases_on_balls = models.IntegerField(null=True, blank=True)  # 四球
    intentional_walks = models.IntegerField(null=True, blank=True)  # 敬遠
    hit_by_pitch = models.IntegerField(null=True, blank=True)  # 死球
    strike_outs = models.IntegerField(null=True, blank=True)  # 三振
    grounded_into_double_plays = models.IntegerField(null=True, blank=True)  # 併殺
    interferences = models.IntegerField(null=True, blank=True)  # 妨
    batting_average = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)  # 打率
    on_base_percentage = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)  # 出塁率
    slugging_percentage = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)  # 長打率
    ops = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)  # OPS
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'player_batting_records'  # 使用するテーブル名を指定
        unique_together = ('player', 'year')  # 選手と年度の組み合わせは一意

    def __str__(self):
        return f"{self.player.name} ({self.year})"

# 選手守備記録
class PlayerFieldingRecord(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.IntegerField()  # 年度（シーズン）
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    games = models.IntegerField(null=True, blank=True)  # 出場試合
    put_outs = models.IntegerField(null=True, blank=True)  # 刺殺
    assists = models.IntegerField(null=True, blank=True)  # 捕殺
    errors = models.IntegerField(null=True, blank=True)  # 失策
    double_plays = models.IntegerField(null=True, blank=True)  # 併殺
    fielding_percentage = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)  # 守備率
    passed_balls = models.IntegerField(null=True, blank=True)  # 捕逸
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'player_fielding_records'  # 使用するテーブル名を指定
        unique_together = ('player', 'year', 'position')  # 選手と年度とポジションの組み合わせは一意

    def __str__(self):
        return f"{self.player.name} ({self.year})"
