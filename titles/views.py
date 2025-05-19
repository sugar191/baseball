from django.shortcuts import render, get_object_or_404
from .models import Title, PlayerTitleView
from positions.utils.constants import POSITION_LABELS


# Create your views here.
def title_list(request):
    titles = Title.objects.all().order_by("sort_order")

    return render(
        request,
        "titles/title_list.html",
        {
            "titles": titles,
        },
    )


def title_detail(request, title_id):
    title = get_object_or_404(Title, id=title_id)
    player_titles = PlayerTitleView.objects.filter(title_id=title_id)

    return render(
        request,
        "titles/title_detail.html",
        {
            "title": title,
            "player_titles": player_titles,
            "position_labels": POSITION_LABELS,  # 追加
        },
    )
