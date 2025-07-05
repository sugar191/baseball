from django.shortcuts import render
from datetime import date
from players.models import PlayerLatestSummary
from teams.models import TeamSeason, League
from games.models import Game


def league_rank(league_id):
    league = League.objects.get(id=league_id)
    teams = TeamSeason.objects.filter(league=league_id).order_by(
        "league__sort_order", "sort_order"
    )

    top_team = teams.first()

    # 各チームにゲーム差を付与
    for team in teams:
        if team.win is not None and team.lose is not None:
            team.game_behind = (
                (top_team.win - team.win) + (team.lose - top_team.lose)
            ) / 2
        else:
            team.game_behind = None

    return league, teams


# Create your views here.
# 選手一覧を表示するビュー
def top_page(request):
    today = date.today()
    ce_league, ce_teams = league_rank(1)
    pa_league, pa_teams = league_rank(2)
    players = PlayerLatestSummary.objects.filter(
        player_birthday__month=today.month, player_birthday__day=today.day
    ).order_by("-player_birthday")
    games = Game.objects.filter(date=today)

    return render(
        request,
        "home/top.html",
        {
            "ce_league": ce_league,
            "pa_league": pa_league,
            "ce_teams": ce_teams,
            "pa_teams": pa_teams,
            "players": players,
            "games": games,
        },
    )
