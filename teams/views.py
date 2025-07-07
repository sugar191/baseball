from django.shortcuts import render, get_object_or_404
from django.db.models import Q, IntegerField
from django.db.models.functions import Cast
from .models import Team, Organization
from players.models import Player, PlayerRecordView
from seasons.models import Season
from records.models import PlayerCommonRecord


def safe_int(value, default=9999):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


# 選手一覧を表示するビュー
def team_list(request):
    qs = Team.objects.all()

    organization_id = request.GET.get("organization", "")
    organizations = Organization.objects.all()

    filters = Q()  # 初期化
    if organization_id:
        filters &= Q(league__organization_id=organization_id)

    teams = qs.filter(filters).order_by("-is_select")

    return render(
        request,
        "teams/team_list.html",
        {
            "teams": teams,
            "organizations": organizations,
        },
    )


def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    seasons = Season.objects.filter(
        organization_id=team.league.organization_id
    ).order_by("-year")

    # season_id を取得（空の可能性もある）
    selected_season_id = request.GET.get("season_id")

    if selected_season_id:
        records = PlayerRecordView.objects.filter(
            team_id=team_id, season_id=selected_season_id
        )

        # ソート
        sorted_players = sorted(
            records,
            key=lambda p: (
                p.is_training,
                p.position_order if p.position_order else 999,
                safe_int(p.common_record_number),
            ),
        )
    else:
        sorted_players = []

    return render(
        request,
        "teams/team_detail.html",
        {"team": team, "players": sorted_players, "seasons": seasons},
    )
