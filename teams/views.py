from django.shortcuts import render, get_object_or_404
from django.db.models import Q, IntegerField
from django.db.models.functions import Cast
from .models import Team, Organization
from players.models import PlayerLatestSummary


# 選手一覧を表示するビュー
def team_list(request):
    qs = Team.objects.all()

    organization_id = request.GET.get("organization", "")
    organizations = Organization.objects.all()

    filters = Q()  # 初期化
    if organization_id:
        filters &= Q(league__organization_id=organization_id)

    teams = qs.filter(filters)

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
    players = (
        PlayerLatestSummary.objects.filter(team_id=team_id)
        .annotate(number_as_int=Cast("common_record_number", IntegerField()))
        .order_by("player_category_order", "position_order", "number_as_int")
    )

    return render(
        request,
        "teams/team_detail.html",
        {"team": team, "players": players},
    )
