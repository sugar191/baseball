from django.db.models import OuterRef, Subquery, Exists, Q
from django.shortcuts import render, get_object_or_404
from .models import Player, PlayerCommonRecord

# 「2億5千万」のような日本語表記に変換する関数
def format_japanese_number(num):
    if num == int(num):
        formatted_num = int(num)  # 整数にする
    else:
        formatted_num = float(num)  # floatに変換して余分なゼロを取り除く

    units = [("億", 10**8), ("万", 10**4), ("", 1)]
    result = []

    for unit, value in units:
        if formatted_num >= value:
            result.append(f"{formatted_num // value}{unit}")
            formatted_num %= value

    return "".join(result)

# 16進カラーコードをRGB形式に変換
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return ', '.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))

# 選手一覧を表示するビュー
def player_list(request):
    query = request.GET.get('q', '')  # 検索キーワード取得
    
    latest_records = PlayerCommonRecord.objects.filter(
        player=OuterRef('id')
    ).order_by('-year').values('id')[:1]

    players = Player.objects.annotate(
        latest_record_id=Subquery(latest_records)
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
        height = format_japanese_number(player.height) + " cm" if player.height else '不明'
        weight = format_japanese_number(player.weight) + " kg" if player.weight else '不明'
        wikipedia_url = "https://ja.wikipedia.org/wiki/" + player.wikipedia_parameter if player.wikipedia_parameter else ''
        youtube_url = "https://www.youtube.com/watch?v=" + player.youtube_parameter if player.youtube_parameter else ''

        # 最新年度のレコードを取得
        latest_record = PlayerCommonRecord.objects.filter(player=player).order_by('-year').first()
        name = latest_record.registered_name if latest_record else None
        team_logo = latest_record.team.logo if latest_record else None
        team_color = hex_to_rgb(latest_record.team.color) if latest_record else None
        number = latest_record.number if latest_record else None
        salary = f"{format_japanese_number(latest_record.salary)}{latest_record.currency.name}" if latest_record.salary else '不明'

        player_data.append({
            'id': player.id,
            'name': name,
            'nickname': player.nickname,
            'team_logo': team_logo,
            'number': number,
            'position': player.main_position_category,
            'birthday': player.birthday,
            'age': player.age,
            'throw_bat': player.throw_bat,
            'height': height,
            'weight': weight,
            'place': player.place,
            'salary': salary,
            'color': team_color,
            'marriage': player.marriage,
            'hobby': player.hobby,
            'specialty': player.specialty,
            'wikipedia': wikipedia_url,
            'youtube': youtube_url,
        })

    return render(request, 'players/player_list.html', {'players': player_data, 'query': query})

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return render(request, 'players/player_detail.html', {'player': player})