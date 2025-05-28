from django.shortcuts import render, get_object_or_404
from .models import Game
from seasons.models import Season


# Create your views here.
def game_list(request):
    games = Game.objects.all()

    if request.GET.get("status_null") == "1":
        games = games.filter(game_status__isnull=True)

    return render(
        request,
        "games/game_list.html",
        {
            "games": games,
        },
    )
