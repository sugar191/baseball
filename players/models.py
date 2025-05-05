from django.db import models
from django.utils import timezone
from commons.models import Place
from positions.models import PositionCategory
from teams.models import Team

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

# 選手テーブル
class Player(models.Model):
    name = models.CharField("氏名", max_length=50, null=False, blank=False)  # 選手名
    furigana = models.CharField("ふりがな", max_length=50, null=True, blank=True)  # 選手名(ふりがな)
    nickname = models.CharField("通称", max_length=50, null=True, blank=True)  # 通称
    birthday = models.DateField("誕生日", null=True, blank=True)  # 生年月日
    place = models.ForeignKey(Place, verbose_name="出身地", on_delete=models.RESTRICT, null=True, blank=True)  # 出身地をForeignKeyで参照
    height = models.DecimalField("身長", max_digits=5, decimal_places=2, null=True, blank=True)  # 身長（cm）
    weight = models.DecimalField("体重", max_digits=5, decimal_places=2, null=True, blank=True)  # 体重（kg）
    is_married = models.BooleanField("結婚", null=True, blank=True) #  結婚しているかどうか
    partner = models.CharField("結婚相手", max_length=50, null=True, blank=True) #  結婚相手
    hobby = models.CharField("趣味", max_length=50, null=True, blank=True) #  趣味
    specialty = models.CharField("特技", max_length=50, null=True, blank=True) #  特技
    throwing_hand = models.ForeignKey(HandThrowing, verbose_name="利腕", on_delete=models.RESTRICT, null=True, blank=True)  # 投手の手をForeignKeyで参照
    batting_hand = models.ForeignKey(HandBatting, verbose_name="利腕", on_delete=models.RESTRICT, null=True, blank=True)  # 打者の手をForeignKeyで参照
    main_position_category = models.ForeignKey(PositionCategory, verbose_name="ポジション", on_delete=models.RESTRICT, null=True, blank=True)  # ポジションをForeignKeyで参照
    favorite_team = models.ForeignKey(Team, verbose_name="ファン球団", on_delete=models.RESTRICT, null=True, blank=True)  # ファン球団をForeignKeyで参照
    wikipedia_parameter = models.CharField("Wikipedia", max_length=250, null=True, blank=True) #  WikipediaURLパラメータ
    usukoi_parameter = models.IntegerField("日本プロ野球記録", null=True, blank=True)  # 日本プロ野球記録サイトのパラメータ
    youtube_parameter = models.CharField("YouTube", max_length=250, null=True, blank=True) #  Youtubeパラメータ
    remarks = models.CharField("備考", max_length=250, null=True, blank=True) #  備考
    created_at = models.DateTimeField("作成日時", default=timezone.now)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        db_table = 'players'  # 使用するテーブル名を指定

    def __str__(self):
        return self.name

    # 年齢を計算するプロパティ
    @property
    def age(self):
        from datetime import date
        if self.birthday:
            today = date.today()
            return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return None

    # 利腕を表示するプロパティ
    @property
    def throw_bat(self):
        return f"{self.throwing_hand}{self.batting_hand}"

    # 婚姻を表示するプロパティ
    @property
    def marriage(self):
        if self.is_married is True:
            return f"既婚 ({self.partner})" if self.partner else "既婚"
        elif self.is_married is False:
            return "独身"
        return "不明"

# 検索ビュー
class PlayerLatestSummary(models.Model):
    player_id = models.IntegerField(primary_key=True)  # 必ず主キーを指定
    player_name = models.CharField(max_length=50, null=False, blank=False)  # 選手名
    player_furigana = models.CharField(max_length=50, null=True, blank=True)  # 選手名(ふりがな)
    player_nickname = models.CharField(max_length=50, null=True, blank=True)  # 通称
    player_birthday = models.DateField(null=True, blank=True)  # 生年月日
    player_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 身長（cm）
    player_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 体重（kg）
    player_is_married = models.BooleanField(null=True, blank=True) #  結婚しているかどうか
    player_partner = models.CharField(max_length=50, null=True, blank=True) #  結婚相手
    player_hobby = models.CharField(max_length=50, null=True, blank=True) #  趣味
    player_specialty = models.CharField(max_length=50, null=True, blank=True) #  特技
    player_wikipedia_parameter = models.CharField(max_length=250, null=True, blank=True) #  WikipediaURLパラメータ
    player_usukoi_parameter = models.IntegerField(null=True, blank=True)  # 日本プロ野球記録サイトのパラメータ
    player_youtube_parameter = models.CharField(max_length=250, null=True, blank=True) #  Youtubeパラメータ
    player_remarks = models.CharField(max_length=250, null=True, blank=True) #  備考
    place_id = models.IntegerField()
    place_name = models.CharField(max_length=10)  # 場所名
    throwing_id = models.IntegerField()
    throwing_name = models.CharField(max_length=10)
    batting_id = models.IntegerField()
    batting_name = models.CharField(max_length=10)
    position_category_id = models.IntegerField()
    position_category_name = models.CharField(max_length=50, null=False, blank=False)  # 名前
    position_order = models.IntegerField(default=0)  # 表示順
    player_career_remarks = models.CharField(max_length=50, null=True, blank=True)
    career_version_id = models.IntegerField()
    career_version_name = models.CharField(max_length=50)
    career_id = models.IntegerField()
    career_category_id = models.IntegerField()
    career_category_label = models.CharField(max_length=10)
    player_draft_rank = models.IntegerField()
    player_draft_team = models.IntegerField()
    player_draft_miss_count = models.IntegerField()
    draft_year = models.IntegerField()
    draft_category_name = models.CharField(max_length=50, null=False, blank=False)  # 名前
    common_record_year = models.IntegerField()
    common_record_number = models.CharField(max_length=5, null=True, blank=True)  # 背番号
    common_record_registered_name = models.CharField(max_length=50, null=True, blank=True)  # 登録名
    common_record_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # 最大12桁、2桁小数点
    currency_name = models.CharField(max_length=30, null=False, blank=False)  # 通貨
    team_id = models.IntegerField()
    team_name = models.CharField(max_length=50)
    team_logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)  # 球団ロゴ画像
    team_order = models.IntegerField(default=0)  # 表示順（順位に基づく）
    team_color = models.CharField(max_length=50, null=True, blank=True) # 球団カラーのカラーコード
    league_order = models.IntegerField()
    organization_order = models.IntegerField()
    pitching_year = models.IntegerField()
    pitching_games = models.IntegerField(null=True, blank=True)  # 登板
    pitching_wins = models.IntegerField(null=True, blank=True)  # 勝利
    pitching_loses = models.IntegerField(null=True, blank=True)  # 敗戦
    pitching_saves = models.IntegerField(null=True, blank=True)  # セーブ
    pitching_holds = models.IntegerField(null=True, blank=True)  # ホールド
    pitching_strike_outs = models.IntegerField(null=True, blank=True)  # 奪三振
    pitching_earned_run_average = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 防御率
    batting_year = models.IntegerField()
    batting_plate_appearances = models.IntegerField(null=True, blank=True)  # 打席
    batting_home_runs = models.IntegerField(null=True, blank=True)  # 本塁打
    batting_runs_batted_in = models.IntegerField(null=True, blank=True)  # 打点
    batting_stolen_bases = models.IntegerField(null=True, blank=True)  # 盗塁
    batting_average = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)  # 打率

    class Meta:
        managed = False  # DjangoがCREATE TABLEしないように
        db_table = 'player_latest_summary'

    def __str__(self):
        return f"{self.player_name}"

    # 年齢を計算するプロパティ
    @property
    def age(self):
        from datetime import date
        if self.player_birthday:
            today = date.today()
            return today.year - self.player_birthday.year - ((today.month, today.day) < (self.player_birthday.month, self.player_birthday.day))
        return None

    # 利腕を表示するプロパティ
    @property
    def throw_bat(self):
        return f"{self.throwing_name}{self.batting_name}"

    # 婚姻を表示するプロパティ
    @property
    def marriage(self):
        if self.player_is_married is True:
            return f"既婚 ({self.player_partner})" if self.player_partner else "既婚"
        elif self.player_is_married is False:
            return "独身"
        return None