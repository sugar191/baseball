from django.shortcuts import render
from .models import Season


# Create your views here.
def season_list(request):
    seasons = Season.objects.filter(year__isnull=False).order_by(
        "organization", "-year"
    )

    return render(
        request,
        "seasons/season_list.html",
        {
            "seasons": seasons,
        },
    )
