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

# 経歴カテゴリ
class CareerCategory(models.Model):
    name = models.CharField(max_length=10)
    label = models.CharField(max_length=10, null=True, blank=True)
    sort_order = models.IntegerField()

    class Meta:
        db_table = 'career_category'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# 経歴
class Career(models.Model):
    name = models.CharField(max_length=50)
    career_category = models.ForeignKey(CareerCategory, on_delete=models.RESTRICT, null=True, blank=True)
    is_private = models.BooleanField(null=True)
    place = models.ForeignKey(Place, on_delete=models.RESTRICT, null=True, blank=True)
    wikipedia_parameter1 = models.CharField(max_length=500, null=True, blank=True) #  WikipediaURLパラメータ
    wikipedia_parameter2 = models.CharField(max_length=500, null=True, blank=True) #  WikipediaURLパラメータ

    class Meta:
        db_table = 'career'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# 経歴バージョン
class CareerVersion(models.Model):
    name = models.CharField(max_length=50)
    career = models.ForeignKey(Career, on_delete=models.RESTRICT, null=True, blank=True)
    version = models.IntegerField(default=0)

    class Meta:
        db_table = 'career_version'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

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

# ポジション
class Position(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # 名前
    position_category = models.ForeignKey(PositionCategory, on_delete=models.CASCADE, null=True, blank=True)
    sort_order = models.IntegerField(default=0)  # 表示順

    class Meta:
        db_table = 'position'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# タイトル
class Title(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # 名前
    sort_order = models.IntegerField(default=0)  # 表示順

    class Meta:
        db_table = 'titles'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

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
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 身長（cm）
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 体重（kg）
    is_married = models.BooleanField(null=True, blank=True) #  結婚しているかどうか
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

    # 利腕を表示するプロパティ
    @property
    def throw_bat(self):
        throwing = f"{self.throwing_hand.name}投" if self.throwing_hand else None
        batting = f"{self.batting_hand.name}打" if self.batting_hand else None
        return f"{throwing}{batting}"

    # 婚姻を表示するプロパティ
    @property
    def marriage(self):
        if self.is_married == 1:
            marriage = '既婚'
            if self.partner and self.partner != '':
                marriage = marriage + ' (' + self.partner + ')'
        elif self.is_married == 0:
            marriage = '独身'
        else:
            marriage = None
        return marriage  # これが抜けていると None が返る

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

# 経歴
class PlayerCareer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    career_version = models.ForeignKey(CareerVersion, on_delete=models.RESTRICT, null=True, blank=True)
    sort_order = models.IntegerField()
    remarks = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'player_career'  # 使用するテーブル名を指定

    def __str__(self):
        return f"{self.player.name} ({self.career.name})"

# 選手タイトル
class PlayerTitle(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.IntegerField()  # 年度（シーズン）
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'player_titles'  # 使用するテーブル名を指定

    def __str__(self):
        return f"{self.player.name}"

# ドラフト種別
class DraftCategory(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # 名前
    sort_order = models.IntegerField(default=0)  # 表示順

    class Meta:
        db_table = 'draft_categories'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

# ドラフト
class Draft(models.Model):
    year = models.IntegerField()  # 年度（シーズン）
    draft_category = models.ForeignKey(DraftCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'drafts'  # 使用するテーブル名を指定

    def __str__(self):
        return f"{self.year}"

# 選手ドラフト
class PlayerDraft(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # 所属球団
    rank = models.IntegerField()
    position_category = models.ForeignKey(PositionCategory, on_delete=models.RESTRICT, null=True, blank=True)
    is_reverse_nomination = models.BooleanField(null=True, blank=True)
    is_hit = models.BooleanField(null=True, blank=True)
    miss_count = models.IntegerField()
    is_joined = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'player_drafts'  # 使用するテーブル名を指定

    def __str__(self):
        return f"{self.player.name} ({self.draft})"