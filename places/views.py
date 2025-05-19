from django.shortcuts import render, get_object_or_404
from .models import Place
from players.models import PlayerLatestSummary


# 出身地一覧を表示するビュー
def place_list(request):
    places = Place.objects.all()

    return render(
        request,
        "places/place_list.html",
        {
            "places": places,
        },
    )


def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    players = PlayerLatestSummary.objects.filter(place_id=place_id)

    return render(
        request,
        "places/place_detail.html",
        {
            "place": place,
            "players": players,
        },
    )
