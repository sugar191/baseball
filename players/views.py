from django.db.models import OuterRef, Subquery, Q, Max, IntegerField
from django.shortcuts import render, get_object_or_404, redirect
from .models import Player, PlayerCommonRecord, PlayerBattingRecord, PlayerPitchingRecord, PlayerCareer, PlayerDraft, PlayerTitle, PlayerLatestSummary
from .forms import PlayerForm, PlayerCommonRecordFormSet

# 選手一覧を表示するビュー
def player_list(request):
    # 検索キーワード取得
    query = request.GET.get('q', '')
    
    player_data = PlayerLatestSummary.objects.filter(
        Q(player_name__icontains=query) |
        Q(player_furigana__icontains=query) |
        Q(common_record_registered_name__icontains=query)
    ).order_by(
        'league_order',
        'team_order',
        'position_order',
        'common_record_number'
    )

    return render(request, 'players/player_list.html', {'players': player_data, 'query': query})

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    common_records = PlayerCommonRecord.objects.filter(player=player).order_by('year')
    batting_records = PlayerBattingRecord.objects.filter(player=player).order_by('year')
    pitching_records = PlayerPitchingRecord.objects.filter(player=player).order_by('year')
    careers = PlayerCareer.objects.filter(player=player).order_by('sort_order')
    drafts = PlayerDraft.objects.filter(player=player).order_by('draft')
    titles = PlayerTitle.objects.filter(player=player).order_by('year', 'title')
    return render(request, 'players/player_detail.html', {
        'player': player, 
        'commons': common_records, 
        'battings': batting_records, 
        'pitchings': pitching_records,
        'careers': careers,
        'drafts': drafts,
        'titles': titles,
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

def player_edit(request, pk):
    player = get_object_or_404(Player, pk=pk)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        formset = PlayerCommonRecordFormSet(request.POST, instance=player)
        if form.is_valid():
            form.save()
            formset.save()
            return redirect('player_detail', pk=player.pk)  # 詳細ページへリダイレクト
    else:
        form = PlayerForm(instance=player)
        formset = PlayerCommonRecordFormSet(instance=player)
    return render(request, 'players/player_edit.html', {'form': form, 'formset': formset, 'player': player})