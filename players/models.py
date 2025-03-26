from django.db import models
from django.utils import timezone

# 出身地テーブル
class Place(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # 場所名
    sort_order = models.IntegerField(default=0)  # 表示順
    is_foreign = models.BooleanField(default=True)  #海外かどうか

    class Meta:
        db_table = 'places'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

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
        return self.year

# 投手手のマスターテーブル
class HandThrowing(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'hands_throwing'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# 打席手のマスターテーブル
class HandBatting(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'hands_batting'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# ポジション種別
class PositionCategory(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # 名前
    sort_order = models.IntegerField(default=0)  # 表示順

    class Meta:
        db_table = 'position_categories'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# リーグテーブル
class League(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False)
    sort_order = models.IntegerField(default=0)  # 表示順を決めるフィールド

    class Meta:
        db_table = 'leagues'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# 球団テーブル
class Team(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='team_logos/')  # 球団ロゴ画像
    league = models.ForeignKey(League, related_name='teams', on_delete=models.CASCADE)  # リーグとの関連
    sort_order = models.IntegerField(default=0)  # 表示順（順位に基づく）
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.league.name})"

    class Meta:
        db_table = 'teams'  # 使用するテーブル名を指定
        ordering = ['league', 'sort_order']  # リーグごと、シーズン順位でソート

# 選手テーブル
class Player(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # 選手名
    furigana = models.CharField(max_length=50, null=True, blank=True)  # 選手名(ふりがな)
    nickname = models.CharField(max_length=50, null=True, blank=True)  # 通称
    birthday = models.DateField(null=True, blank=True)  # 生年月日
    birth_year = models.IntegerField(null=True, blank=True)  # 年のみを保存
    birth_month = models.IntegerField(null=True, blank=True)  # 月のみを保存
    place = models.ForeignKey(Place, on_delete=models.RESTRICT, null=True, blank=True)  # 出身地をForeignKeyで参照
    height = models.IntegerField(null=True, blank=True)  # 身長（cm）
    weight = models.IntegerField(null=True, blank=True)  # 体重（kg）
    is_married = models.BooleanField(default=True) #  結婚しているかどうか
    partner = models.CharField(max_length=50, null=True, blank=True) #  結婚相手
    hobby = models.CharField(max_length=50, null=True, blank=True) #  趣味
    specialty = models.CharField(max_length=50, null=True, blank=True) #  特技
    throwing_hand = models.ForeignKey(HandThrowing, on_delete=models.RESTRICT, null=True, blank=True)  # 投手の手をForeignKeyで参照
    batting_hand = models.ForeignKey(HandBatting, on_delete=models.RESTRICT, null=True, blank=True)  # 打者の手をForeignKeyで参照
    main_position_category = models.ForeignKey(PositionCategory, on_delete=models.RESTRICT, null=True, blank=True)  # ポジションをForeignKeyで参照
    favorite_team = models.ForeignKey(Team, on_delete=models.RESTRICT, null=True, blank=True)  # ファン球団をForeignKeyで参照
    wikipedia_parameter = models.CharField(max_length=250, null=True, blank=True) #  WikipediaURLパラメータ
    usukoi_parameter = models.IntegerField(null=True, blank=True)  # 日本プロ野球記録サイトのパラメータ
    youtube_parameter = models.CharField(max_length=250, null=True, blank=True) #  Youtubeパラメータ
    remarks = models.CharField(max_length=250, null=True, blank=True) #  備考
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'players'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name
    
    # 年齢を計算するプロパティ
    @property
    def age(self):
        from datetime import date
        if self.birthday:
            return date.today().year - self.birthday.year
        return None

    # 投打表記（右投右打など）を作成するプロパティ
    @property
    def throw_bat_display(self):
        throwing = self.throwing_hand.name if self.throwing_hand else "不明"
        batting = self.batting_hand.name if self.batting_hand else "不明"
        return f"{throwing}投{batting}打"

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

    def __str__(self):
        return f"{self.player.name} ({self.year})"