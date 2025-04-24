import re
from datetime import date
from django.db.models import Q, Value
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import Replace
from .models import Player, PlayerCommonRecord, PlayerBattingRecord, PlayerPitchingRecord, PlayerCareer, PlayerDraft, PlayerTitle, PlayerLatestSummary, Team, Place, PositionCategory, Career, HandBatting, HandThrowing
from .forms import PlayerForm, PlayerCommonRecordFormSet

# 選手一覧を表示するビュー
def player_list(request):
    # 検索キーワード取得
    query = request.GET.get('q', '')
    name = request.GET.get('name', '')
    nickname = request.GET.get('nickname', '')
    number = request.GET.get('number', '')
    team_id = request.GET.get('team', '')
    place_id = request.GET.get('birthplace', '')
    position_category_id = request.GET.get('position_category', '')
    career_id = request.GET.get('career', '')
    salary_min = request.GET.get('salary_min', '')
    salary_max = request.GET.get('salary_max', '')
    year = request.GET.get('year', '')
    rank = request.GET.get('rank', '')
    birth_year = request.GET.get('birth_year', '')
    pitching = request.GET.get('pitching', '')
    batting = request.GET.get('batting', '')

    # スペースを除去（全角・半角）
    query_no_space = re.sub(r'\s+', '', query)
    name_no_space = re.sub(r'\s+', '', name)

    # annotate でスペースなしの比較用フィールドを追加
    qs = PlayerLatestSummary.objects.annotate(
        name_no_space=Replace(Replace('player_name', Value(' '), Value('')), Value('　'), Value('')),
        furigana_no_space=Replace(Replace('player_furigana', Value(' '), Value('')), Value('　'), Value('')),
        nickname_no_space=Replace(Replace('player_nickname', Value(' '), Value('')), Value('　'), Value('')),
        registered_name_no_space=Replace(Replace('common_record_registered_name', Value(' '), Value('')), Value('　'), Value(''))
    )

    filters = Q(name_no_space__icontains=query_no_space) |\
        Q(furigana_no_space__icontains=query_no_space) |\
        Q(nickname_no_space__icontains=query_no_space) |\
        Q(registered_name_no_space__icontains=query_no_space) |\
        Q(player_partner__icontains=query) |\
        Q(player_hobby__icontains=query) |\
        Q(player_specialty__icontains=query) |\
        Q(player_remarks__icontains=query) |\
        Q(place_name__icontains=query) |\
        Q(throwing_name__icontains=query) |\
        Q(batting_name__icontains=query) |\
        Q(position_category_name__icontains=query) |\
        Q(player_career_remarks__icontains=query) |\
        Q(career_version_name__icontains=query) |\
        Q(career_category_label__icontains=query) |\
        Q(draft_category_name__icontains=query) |\
        Q(common_record_number=query) |\
        Q(currency_name__icontains=query) |\
        Q(team_name__icontains=query)

    if name:
        filters &= Q(name_no_space__icontains=name_no_space) |\
            Q(furigana_no_space__icontains=name_no_space) |\
            Q(registered_name_no_space__icontains=name_no_space)

    if nickname:
        filters &= Q(nickname_no_space__icontains=nickname)

    if number:
        filters &= Q(common_record_number=number)

    if team_id:
        filters &= Q(team_id=team_id)

    if place_id:
        filters &= Q(place_id=place_id)

    if position_category_id:
        filters &= Q(position_category_id=position_category_id)

    if career_id:
        filters &= Q(career_id=career_id)

    if salary_min:
        try:
            salary_min_int = int(salary_min) * 10000
            filters &= Q(common_record_salary__gte=salary_min_int)
        except ValueError:
            pass  # 無効な入力は無視

    if salary_max:
        try:
            salary_max_int = int(salary_max) * 10000
            filters &= Q(common_record_salary__lte=salary_max_int)
        except ValueError:
            pass  # 無効な入力は無視

    if year:
        filters &= Q(draft_year=year)

    if rank:
        filters &= Q(player_draft_rank=rank)

    if birth_year:
        try:
            birth_year_int = int(birth_year)
            fiscal_start = date(birth_year_int, 4, 1)
            fiscal_end = date(birth_year_int + 1, 3, 31)
            filters &= Q(player_birthday__range=(fiscal_start, fiscal_end))
        except ValueError:
            pass

    if pitching:
        filters &= Q(throwing_id=pitching)

    if batting:
        filters &= Q(batting_id=batting)

    player_data = qs.filter(filters).order_by(
        'league_order',
        'team_order',
        'position_order',
        'common_record_number'
    )

    teams = Team.objects.filter(is_select = True)
    places = Place.objects.all()
    position_categories = PositionCategory.objects.all()
    careers = Career.objects.all()
    throwings = HandThrowing.objects.all()
    battings = HandBatting.objects.all()

    return render(request, 'players/player_list.html', {
        'players': player_data,
        'teams': teams,
        'places': places,
        'position_categories': position_categories,
        'battings': battings,
        'throwings': throwings,
        'careers': careers,
        'query': query
    })

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