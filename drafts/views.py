from collections import defaultdict
from django.shortcuts import render
from django.db.models import Count
from .models import Draft, PlayerDraftView
import collections

# 選手一覧を表示するビュー
def draft_list(request):
    drafts = Draft.objects.values('year').annotate(
        count=Count('id')
    ).order_by('year')

    return render(request, 'drafts/draft_list.html', {
        'drafts': drafts,
    })

def nested_dict():
    return collections.defaultdict(nested_dict)

def convert_to_regular_dict(d):
    if isinstance(d, collections.defaultdict):
        d = {k: convert_to_regular_dict(v) for k, v in d.items()}
    return d

def draft_detail(request, year):
    player_drafts = PlayerDraftView.objects.filter(draft_year=year).order_by(
        'league_order',
        'team_order',
        'draft_category_order',
        'player_draft_rank',
        'player_draft_miss_count'
    )

    grouped_drafts = nested_dict()
    for draft in player_drafts:
        grouped_drafts[draft.league_order][draft.team_name][draft.draft_category_order].setdefault("list", []).append(draft)

    # defaultdictを普通のdictに変換
    grouped_drafts = convert_to_regular_dict(grouped_drafts)

    # "list" キーの中身を取り出す
    for league in grouped_drafts.values():
        for team in league.values():
            for category_order in list(team.keys()):
                team[category_order] = team[category_order]["list"]

    return render(request, 'drafts/draft_detail.html', {
        'year': year,
        'grouped_drafts': grouped_drafts,
    })