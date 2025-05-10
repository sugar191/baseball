import re
from collections import defaultdict, OrderedDict
from datetime import date
from django.core.paginator import Paginator
from django.db.models import (
    Q,
    Value,
    Count,
    F,
    ExpressionWrapper,
    IntegerField,
    Case,
    When,
)
from django.db.models.functions import Replace, ExtractYear, ExtractMonth, ExtractDay
from django.shortcuts import render, get_object_or_404
from .models import Player, PlayerLatestSummary, HandBatting, HandThrowing
from records.models import (
    PlayerCommonRecord,
    PlayerBattingRecord,
    PlayerPitchingRecord,
    PlayerFieldingRecord,
)
from careers.models import Career, PlayerCareer
from drafts.models import PlayerDraft
from titles.models import PlayerTitle
from teams.models import Team
from places.models import Place
from positions.models import PositionCategory
from positions.utils.constants import POSITION_LABELS


# 選手一覧を表示するビュー
def player_list(request):
    # 検索キーワード取得
    query = request.GET.get("q", "")
    name = request.GET.get("name", "")
    nickname = request.GET.get("nickname", "")
    number = request.GET.get("number", "")
    team_id = request.GET.get("team", "")
    place_id = request.GET.get("birthplace", "")
    position_category_id = request.GET.get("position_category", "")
    career_id = request.GET.get("career", "")
    salary_min = request.GET.get("salary_min", "")
    salary_max = request.GET.get("salary_max", "")
    year = request.GET.get("year", "")
    rank = request.GET.get("rank", "")
    birth_year = request.GET.get("birth_year", "")
    pitching = request.GET.get("pitching", "")
    batting = request.GET.get("batting", "")

    # スペースを除去（全角・半角）
    query_no_space = re.sub(r"\s+", "", query)
    name_no_space = re.sub(r"\s+", "", name)

    # annotate でスペースなしの比較用フィールドを追加
    qs = PlayerLatestSummary.objects.annotate(
        name_no_space=Replace(
            Replace("player_name", Value(" "), Value("")), Value("　"), Value("")
        ),
        furigana_no_space=Replace(
            Replace("player_furigana", Value(" "), Value("")), Value("　"), Value("")
        ),
        nickname_no_space=Replace(
            Replace("player_nickname", Value(" "), Value("")), Value("　"), Value("")
        ),
        registered_name_no_space=Replace(
            Replace("common_record_registered_name", Value(" "), Value("")),
            Value("　"),
            Value(""),
        ),
    )

    filters = (
        Q(name_no_space__icontains=query_no_space)
        | Q(furigana_no_space__icontains=query_no_space)
        | Q(nickname_no_space__icontains=query_no_space)
        | Q(registered_name_no_space__icontains=query_no_space)
        | Q(player_partner__icontains=query)
        | Q(player_hobby__icontains=query)
        | Q(player_specialty__icontains=query)
        | Q(player_remarks__icontains=query)
        | Q(place_name__icontains=query)
        | Q(throwing_name__icontains=query)
        | Q(batting_name__icontains=query)
        | Q(position_category_name__icontains=query)
        | Q(player_career_remarks__icontains=query)
        | Q(career_version_name__icontains=query)
        | Q(career_category_label__icontains=query)
        | Q(draft_category_name__icontains=query)
        | Q(common_record_number=query)
        | Q(currency_name__icontains=query)
        | Q(team_name__icontains=query)
    )

    if name:
        filters &= (
            Q(name_no_space__icontains=name_no_space)
            | Q(furigana_no_space__icontains=name_no_space)
            | Q(registered_name_no_space__icontains=name_no_space)
        )

    if nickname:
        filters &= Q(nickname_no_space__icontains=nickname)

    if number:
        filters &= Q(common_record_number=number)

    if team_id:
        filters &= Q(team_id=team_id)

    if place_id:
        filters &= Q(place_id=place_id)

    if position_category_id:
        filters &= Q(position_category_id=position_category_id)

    if career_id:
        filters &= Q(career_id=career_id)

    if salary_min:
        try:
            salary_min_int = int(salary_min) * 10000
            filters &= Q(common_record_salary__gte=salary_min_int)
        except ValueError:
            pass  # 無効な入力は無視

    if salary_max:
        try:
            salary_max_int = int(salary_max) * 10000
            filters &= Q(common_record_salary__lte=salary_max_int)
        except ValueError:
            pass  # 無効な入力は無視

    if year:
        filters &= Q(draft_year=year)

    if rank:
        filters &= Q(player_draft_rank=rank)

    if birth_year:
        try:
            birth_year_int = int(birth_year)
            fiscal_start = date(birth_year_int, 4, 1)
            fiscal_end = date(birth_year_int + 1, 3, 31)
            filters &= Q(player_birthday__range=(fiscal_start, fiscal_end))
        except ValueError:
            pass

    if pitching:
        filters &= Q(throwing_id=pitching)

    if batting:
        filters &= Q(batting_id=batting)

    player_data = qs.filter(filters).order_by(
        "organization_order",
        "league_order",
        "team_order",
        "position_order",
        "common_record_number",
    )

    paginator = Paginator(player_data, 30)  # 30件ずつ
    page_number = request.GET.get("page")  # URLの?page=2などを取得
    page_obj = paginator.get_page(page_number)

    teams = Team.objects.filter(is_select=True)
    places = Place.objects.all()
    position_categories = PositionCategory.objects.all()
    careers = Career.objects.all()
    throwings = HandThrowing.objects.all()
    battings = HandBatting.objects.all()

    # page以外のGETパラメータを抽出してurlencode
    get_params = request.GET.copy()
    if "page" in get_params:
        del get_params["page"]
    querystring = get_params.urlencode()

    return render(
        request,
        "players/player_list.html",
        {
            "players": page_obj,
            "querystring": querystring,
            "teams": teams,
            "places": places,
            "position_categories": position_categories,
            "battings": battings,
            "throwings": throwings,
            "careers": careers,
            "query": query,
        },
    )


def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    common_records = PlayerCommonRecord.objects.filter(player=player).order_by("year")
    mlb_exists = PlayerBattingRecord.objects.filter(player=player, year=9001).exists()
    batting_records = PlayerBattingRecord.objects.filter(player=player).order_by("year")
    pitching_records = PlayerPitchingRecord.objects.filter(player=player).order_by(
        "year"
    )
    fielding_records = PlayerFieldingRecord.objects.filter(player=player).order_by(
        "year", "position_id"
    )
    careers = PlayerCareer.objects.filter(player=player).order_by("sort_order")
    drafts = PlayerDraft.objects.filter(player=player).order_by("draft")
    titles = PlayerTitle.objects.filter(player=player).order_by("year", "title")

    # 年ごとにポジション別にまとめる
    yearly_fielding = defaultdict(list)
    for record in fielding_records:
        yearly_fielding[record.year].append(
            {"position_id": record.position_id, "games": record.games}
        )

    # 各年の出場状況とHTML表示用の文字列を追加
    fielding_summary = {}
    for year, positions in yearly_fielding.items():
        total_games = sum(p["games"] for p in positions)
        summary_parts = []
        for p in positions:
            pos_id = p["position_id"]
            games = p["games"]
            if pos_id in POSITION_LABELS and games > 0:
                label, css_class = POSITION_LABELS[pos_id]
                html = f'<span class="position-badge {css_class}">{label}</span>{games}'
                summary_parts.append(html)
        summary_html = " ".join(summary_parts)
        fielding_summary[year] = {"total_games": total_games, "html": summary_html}

    # 年順にソート
    fielding_summary_ordered = OrderedDict(
        sorted(fielding_summary.items())
    )  # OrderedDictに変換

    # 誕生日を基準に学年の範囲を決定（4月2日始まり〜翌年4月1日）
    birthday = player.birthday

    if birthday.month >= 4:
        # 例えば 1990年4月10日 → 1990年4月2日〜1991年4月1日
        start_date = date(birthday.year, 4, 2)
        end_date = date(birthday.year + 1, 4, 1)
    else:
        # 例えば 1991年1月10日 → 1990年4月2日〜1991年4月1日
        start_date = date(birthday.year - 1, 4, 2)
        end_date = date(birthday.year, 4, 1)

    classmates = PlayerLatestSummary.objects.filter(
        player_birthday__gte=start_date, player_birthday__lte=end_date
    ).exclude(pk=player.pk)

    draft_joined = PlayerDraft.objects.filter(
        player_id=player_id, is_joined=True
    ).first()

    same_time_joined = []
    if draft_joined:
        same_time_joined = PlayerLatestSummary.objects.filter(
            draft_year=draft_joined.draft.year, player_draft_team=draft_joined.team_id
        ).exclude(pk=player.pk)

    return render(
        request,
        "players/player_detail.html",
        {
            "player": player,
            "commons": common_records,
            "mlb_exists": mlb_exists,
            "battings": batting_records,
            "pitchings": pitching_records,
            "fieldings": fielding_summary_ordered,  # そのままリストで渡す
            "careers": careers,
            "drafts": drafts,
            "titles": titles,
            "position_labels": POSITION_LABELS,  # 追加
            "classmates": classmates,
            "same_time_joined": same_time_joined,
        },
    )


def player_year_detail(request, player_id, year):
    player = get_object_or_404(Player, id=player_id)
    titles = PlayerTitle.objects.filter(player=player, year=year)
    common_record = PlayerCommonRecord.objects.filter(player=player, year=year).first()
    batting_record = PlayerBattingRecord.objects.filter(
        player=player, year=year
    ).first()
    pitching_record = PlayerPitchingRecord.objects.filter(
        player=player, year=year
    ).first()
    fielding_record = PlayerFieldingRecord.objects.filter(
        player=player, year=year, games__gt=0
    )
    # 他の必要なデータもここで取得

    return render(
        request,
        "players/player_year_detail.html",
        {
            "player": player,
            "year": year,
            "titles": titles,
            "common_record": common_record,
            "batting_record": batting_record,
            "pitching_record": pitching_record,
            "fielding_record": fielding_record,
            "position_labels": POSITION_LABELS,  # 追加
        },
    )


def generation_list(request):
    players = (
        Player.objects.annotate(
            birth_year=ExtractYear("birthday"),
            birth_month=ExtractMonth("birthday"),
            birth_day=ExtractDay("birthday"),
        )
        .annotate(
            school_year=Case(
                # 4月2日以降生まれなら birth_year を学年として扱う
                When(birth_month__gt=4, then=F("birth_year")),
                When(birth_month=4, birth_day__gte=2, then=F("birth_year")),
                # それ以前は前の年を学年として扱う
                default=ExpressionWrapper(
                    F("birth_year") - 1, output_field=IntegerField()
                ),
            )
        )
        .values("school_year")
        .annotate(count=Count("id"))
        .order_by("school_year")
    )

    return render(request, "players/generation_list.html", {"generations": players})


def generation_players(request, year):
    """
    指定された「学年」に属する選手一覧を表示するビュー
    例: year=1990 の場合、1990/4/2 ～ 1991/4/1 生まれの選手を抽出
    """
    start_date = date(year, 4, 2)
    end_date = date(year + 1, 4, 1)

    players = Player.objects.filter(
        birthday__gte=start_date, birthday__lte=end_date
    ).order_by("birthday")

    return render(
        request,
        "players/generation_players.html",
        {
            "year": year,
            "players": players,
        },
    )
