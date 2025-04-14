from django.db.models import OuterRef, Subquery, Exists, Q
from django.shortcuts import render, get_object_or_404
from .models import Player, PlayerCommonRecord, PlayerBattingRecord, PlayerPitchingRecord

# 16進カラーコードをRGB形式に変換
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return ', '.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))

# 選手一覧を表示するビュー
def player_list(request):
    query = request.GET.get('q', '')  # 検索キーワード取得

    latest_common_records = PlayerCommonRecord.objects.filter(
        player=OuterRef('id')
    ).order_by('-year').values('id')[:1]

    players = Player.objects.annotate(
        latest_record_id=Subquery(latest_common_records)
    ).filter(
        Exists(PlayerCommonRecord.objects.filter(id=OuterRef('latest_record_id'))) &  # AND条件を明示的に指定
        Q(name__icontains=query) | 
        Q(furigana__icontains=query) | 
        Q(playercommonrecord__registered_name__icontains=query)  # 関連テーブルを検索
    ).prefetch_related(
        'playercommonrecord_set__team__league'
    ).select_related(
        'main_position_category'
    ).order_by(
        'playercommonrecord__team__league__sort_order',
        'playercommonrecord__team__sort_order',
        'main_position_category__sort_order',
        'playercommonrecord__number'
    ) if query else Player.objects.all()

    player_data = []
    for player in players:
        wikipedia_url = "https://ja.wikipedia.org/wiki/" + player.wikipedia_parameter if player.wikipedia_parameter else ''
        youtube_url = "https://www.youtube.com/watch?v=" + player.youtube_parameter if player.youtube_parameter else ''

        # 最新年度のレコードを取得
        latest_common_record = PlayerCommonRecord.objects.filter(player=player).order_by('-year').first()
        name = latest_common_record.registered_name if latest_common_record else None
        common_year = latest_common_record.year if latest_common_record else None
        team_logo = latest_common_record.team.logo if latest_common_record else None
        team_color = hex_to_rgb(latest_common_record.team.color) if latest_common_record else None
        number = latest_common_record.number if latest_common_record else None
        salary = latest_common_record.salary if latest_common_record.salary else '不明'
        currency = latest_common_record.currency if latest_common_record.currency else '不明'

        latest_batting_record = PlayerBattingRecord.objects.filter(player=player, year__lt=9000).order_by('-year').first()
        batting_year = latest_batting_record.year if latest_batting_record else None
        average = latest_batting_record.batting_average if latest_batting_record else None
        homerun = latest_batting_record.home_runs if latest_batting_record else None
        rbi = latest_batting_record.runs_batted_in if latest_batting_record else None
        steal = latest_batting_record.stolen_bases if latest_batting_record else None

        latest_pitching_record = PlayerPitchingRecord.objects.filter(player=player, year__lt=9000).order_by('-year').first()
        pitching_year = latest_pitching_record.year if latest_pitching_record else None
        earned_average = latest_pitching_record.earned_run_average if latest_pitching_record else None
        win = latest_pitching_record.wins if latest_pitching_record else None
        lose = latest_pitching_record.loses if latest_pitching_record else None
        save = latest_pitching_record.saves if latest_pitching_record else None
        hold = latest_pitching_record.holds if latest_pitching_record else None
        strike_out = latest_pitching_record.strike_outs if latest_pitching_record else None

        player_data.append({
            'id': player.id,
            'name': name,
            'common_year': common_year,
            'nickname': player.nickname,
            'team_logo': team_logo,
            'number': number,
            'position': player.main_position_category,
            'birthday': player.birthday,
            'age': player.age,
            'throw_bat': player.throw_bat,
            'height': player.height,
            'weight': player.weight,
            'place': player.place,
            'salary': salary,
            'currency': currency,
            'color': team_color,
            'marriage': player.marriage,
            'hobby': player.hobby,
            'specialty': player.specialty,
            'wikipedia': wikipedia_url,
            'youtube': youtube_url,
            'batting_year': batting_year,
            'average': average,
            'homerun': homerun,
            'rbi': rbi,
            'steal': steal,
            'pitching_year': pitching_year,
            'earned_average': earned_average,
            'win': win,
            'lose': lose,
            'save': save,
            'hold': hold,
            'strike_out': strike_out,
        })

    return render(request, 'players/player_list.html', {'players': player_data, 'query': query})

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    common_records = PlayerCommonRecord.objects.filter(player=player).order_by('year')
    batting_records = PlayerBattingRecord.objects.filter(player=player).order_by('year')
    pitching_records = PlayerPitchingRecord.objects.filter(player=player).order_by('year')
    return render(request, 'players/player_detail.html', {
        'player': player, 
        'commons': common_records, 
        'battings': batting_records, 
        'pitchings': pitching_records
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