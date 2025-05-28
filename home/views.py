from django.shortcuts import render
from datetime import date
from players.models import PlayerLatestSummary
from teams.models import TeamSeason, League
from games.models import Game


# Create your views here.
# 選手一覧を表示するビュー
def top_page(request):
    today = date.today()
    ce_league = League.objects.get(id=1)
    pa_league = League.objects.get(id=2)
    ce_teams = TeamSeason.objects.filter(league=1).order_by(
        "league__sort_order", "sort_order"
    )
    pa_teams = TeamSeason.objects.filter(league=2).order_by(
        "league__sort_order", "sort_order"
    )
    players = PlayerLatestSummary.objects.filter(
        player_birthday__month=today.month, player_birthday__day=today.day
    )
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
