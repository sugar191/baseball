from django.shortcuts import render
from datetime import date
from players.models import PlayerLatestSummary
from teams.models import Team
from games.models import Game


# Create your views here.
# 選手一覧を表示するビュー
def top_page(request):
    today = date.today()
    teams = Team.objects.filter(league__lt=3)
    players = PlayerLatestSummary.objects.filter(
        player_birthday__month=today.month, player_birthday__day=today.day
    )
    games = Game.objects.filter(date=today)

    return render(
        request,
        "home/top.html",
        {
            "teams": teams,
            "players": players,
            "games": games,
        },
    )
