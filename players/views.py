import re
from collections import defaultdict, OrderedDict
from datetime import date
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Replace
from django.shortcuts import render, get_object_or_404, redirect
from .models import Player, PlayerCommonRecord, PlayerBattingRecord, PlayerPitchingRecord, PlayerFieldingRecord, PlayerCareer, PlayerDraft, PlayerTitle, PlayerLatestSummary, Team, Place, PositionCategory, Career, HandBatting, HandThrowing
from .forms import PlayerForm, PlayerCommonRecordFormSet
from .utils.constants import POSITION_LABELS

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
        'organization_order',
        'league_order',
        'team_order',
        'position_order',
        'common_record_number'
    )
    
    paginator = Paginator(player_data, 20)  # 20件ずつ
    page_number = request.GET.get('page')  # URLの?page=2などを取得
    page_obj = paginator.get_page(page_number)

    teams = Team.objects.filter(is_select = True)
    places = Place.objects.all()
    position_categories = PositionCategory.objects.all()
    careers = Career.objects.all()
    throwings = HandThrowing.objects.all()
    battings = HandBatting.objects.all()

    # page以外のGETパラメータを抽出してurlencode
    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']
    querystring = get_params.urlencode()

    return render(request, 'players/player_list.html', {
        'players': page_obj,
        'querystring': querystring,
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
    fielding_records = PlayerFieldingRecord.objects.filter(player=player).order_by('year', 'position_id')
    careers = PlayerCareer.objects.filter(player=player).order_by('sort_order')
    drafts = PlayerDraft.objects.filter(player=player).order_by('draft')
    titles = PlayerTitle.objects.filter(player=player).order_by('year', 'title')

    # 年ごとにポジション別にまとめる
    yearly_fielding = defaultdict(list)
    for record in fielding_records:
        yearly_fielding[record.year].append({
            'position_id': record.position_id,
            'games': record.games
        })

    # 各年の出場状況とHTML表示用の文字列を追加
    fielding_summary = {}
    for year, positions in yearly_fielding.items():
        total_games = sum(p['games'] for p in positions)
        if total_games == 0:
            summary_html = '出場無し'
        else:
            summary_parts = []
            for p in positions:
                pos_id = p['position_id']
                games = p['games']
                if pos_id in POSITION_LABELS:
                    label, css_class = POSITION_LABELS[pos_id]
                    html = f'<span class="position-badge {css_class}">{label}</span> {games}'
                    summary_parts.append(html)
            summary_html = ' '.join(summary_parts)
        fielding_summary[year] = {
            'total_games': total_games,
            'html': summary_html
        }

    # 年順にソート
    fielding_summary_ordered = OrderedDict(sorted(fielding_summary.items()))  # OrderedDictに変換

    return render(request, 'players/player_detail.html', {
        'player': player, 
        'commons': common_records, 
        'battings': batting_records, 
        'pitchings': pitching_records,
        'fieldings': fielding_summary_ordered,  # そのままリストで渡す
        'careers': careers,
        'drafts': drafts,
        'titles': titles,
    })

def player_year_detail(request, player_id, year):
    player = get_object_or_404(Player, id=player_id)
    common_record = PlayerCommonRecord.objects.filter(player=player, year=year).first()
    batting_record = PlayerBattingRecord.objects.filter(player=player, year=year).first()
    pitching_record = PlayerPitchingRecord.objects.filter(player=player, year=year).first()
    fielding_record = PlayerFieldingRecord.objects.filter(player=player, year=year)
    # 他の必要なデータもここで取得

    return render(request, 'players/player_year_detail.html', {
        'player': player,
        'year': year,
        'common_record': common_record,
        'batting_record': batting_record,
        'pitching_record': pitching_record,
        'fielding_record': fielding_record,
        'position_labels': POSITION_LABELS,  # 追加
    })

def player_edit(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        common_record_formset = PlayerCommonRecordFormSet(request.POST, instance=player)
        if form.is_valid() and common_record_formset.is_valid():
            form.save()
            common_record_formset.save()
            return redirect('player_detail', player_id=player.pk)  # 詳細ページへリダイレクト
    else:
        form = PlayerForm(instance=player)
        common_record_formset = PlayerCommonRecordFormSet(instance=player)

    return render(request, 'players/player_edit.html', {
        'form': form,
        'formset': common_record_formset,
        'player': player
    })