from django.db.models import OuterRef, Subquery, Exists, Q
from django.shortcuts import render, get_object_or_404
from .models import Player, PlayerCommonRecord, PlayerBattingRecord, PlayerPitchingRecord, PlayerCareer, PlayerDraft

# 選手一覧を表示するビュー
def player_list(request):
    # 検索キーワード取得
    query = request.GET.get('q', '')

    # 検索対象となるPlayerのID一覧
    if query:
        player_ids = Player.objects.filter(
            Q(name__icontains=query) |
            Q(furigana__icontains=query)
        ).values_list('id', flat=True).distinct()
    else:
        player_ids = Player.objects.values_list('id', flat=True)

    # 最新のcommon record idを取得
    latest_common_record_subq = PlayerCommonRecord.objects.filter(
        player=OuterRef('pk')
    ).order_by('-year')

    players = Player.objects.filter(
        id__in=player_ids
    ).annotate(
        latest_number=Subquery(latest_common_record_subq.values('number')[:1]),
        latest_team_sort=Subquery(latest_common_record_subq.values('team__sort_order')[:1]),
        latest_league_sort=Subquery(latest_common_record_subq.values('team__league__sort_order')[:1]),
    ).select_related(
        'main_position_category'
    ).order_by(
        'latest_league_sort',
        'latest_team_sort',
        'main_position_category__sort_order',
        'latest_number'
    )
    player_data = []
    for player in players:

        # 最新年度のレコードを取得
        latest_common_record = PlayerCommonRecord.objects.filter(player=player).order_by('-year').first()
        latest_batting_record = PlayerBattingRecord.objects.filter(player=player, year__lt=9000).order_by('-year').first()
        latest_pitching_record = PlayerPitchingRecord.objects.filter(player=player, year__lt=9000).order_by('-year').first()
        
        # 最終経歴を取得
        latest_career = PlayerCareer.objects.filter(player=player).order_by('-sort_order').first()
        
        # 入団時のドラフト情報を取得
        draft = PlayerDraft.objects.filter(player=player, is_joined=True).first()

        player_data.append({
            'player': player,
            'common_record': latest_common_record,
            'batting_record': latest_batting_record,
            'pitching_record': latest_pitching_record,
            'career': latest_career,
            'draft': draft,
        })

    return render(request, 'players/player_list.html', {'players': player_data, 'query': query})

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    common_records = PlayerCommonRecord.objects.filter(player=player).order_by('year')
    batting_records = PlayerBattingRecord.objects.filter(player=player).order_by('year')
    pitching_records = PlayerPitchingRecord.objects.filter(player=player).order_by('year')
    careers = PlayerCareer.objects.filter(player=player).order_by('sort_order')
    drafts = PlayerDraft.objects.filter(player=player).order_by('draft')
    return render(request, 'players/player_detail.html', {
        'player': player, 
        'commons': common_records, 
        'battings': batting_records, 
        'pitchings': pitching_records,
        'careers': careers,
        'drafts': drafts,
    })

def player_year_detail(request, player_id, year):
    player = get_object_or_404(Player, id=player_id)
    common_record = PlayerCommonRecord.objects.filter(player=player, year=year).first()
    batting_record = PlayerBattingRecord.objects.filter(player=player, year=year).first()
    pitching_record = PlayerPitchingRecord.objects.filter(player=player, year=year).first()
    # 他の必要なデータもここで取得

    return render(request, 'players/player_year_detail.html', {
        'player': player,
        'year': year,
        'common_record': common_record,
        'batting_record': batting_record,
        'pitching_record': pitching_record,
        # 必要な変数を追加
    })
