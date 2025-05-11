from collections import defaultdict
from django.shortcuts import render
from django.db.models import Count
from .models import Draft, PlayerDraftView


# 選手一覧を表示するビュー
def draft_list(request):
    drafts = Draft.objects.values("year").annotate(count=Count("id")).order_by("-year")

    return render(
        request,
        "drafts/draft_list.html",
        {
            "drafts": drafts,
        },
    )


def draft_detail(request, year):
    player_drafts = PlayerDraftView.objects.filter(draft_year=year).order_by(
        "league_order",
        "team_order",
        "draft_category_order",
        "player_draft_rank",
        "player_draft_miss_count",
    )

    grouped_drafts = defaultdict(
        lambda: {"logo": None, "categories": defaultdict(list)}
    )

    for draft in player_drafts:
        team_info = grouped_drafts[draft.team_name]
        team_info["logo"] = draft.team_logo
        team_info["categories"][draft.draft_category_name].append(draft)

    # defaultdict -> dict に変換（ネストも対応）
    grouped_drafts = {
        team_name: {
            "logo": team_info["logo"],
            "categories": dict(team_info["categories"]),
        }
        for team_name, team_info in grouped_drafts.items()
    }

    return render(
        request,
        "drafts/draft_detail.html",
        {
            "year": year,
            "grouped_drafts": grouped_drafts,
        },
    )
