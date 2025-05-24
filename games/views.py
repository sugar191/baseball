from django.shortcuts import render, get_object_or_404
from .models import Game
from seasons.models import Season


# Create your views here.
def game_list(request, season_id):
    season = get_object_or_404(Season, id=season_id)
    games = Game.objects.filter(season=season)

    return render(
        request,
        "games/game_list.html",
        {
            "games": games,
            "season": season,
        },
    )
