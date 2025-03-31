from django.shortcuts import render
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

def hex_to_rgb(hex_color):
    """ 16進カラーコードをRGB形式に変換 """
    hex_color = hex_color.lstrip('#')
    return ', '.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))

# 選手一覧を表示するビュー
def player_list(request):
    players = Player.objects.all()  # Playerモデルから全ての選手を取得

    player_data = []
    for player in players:
        height = format_japanese_number(player.height) + " cm" if player.height else '不明'
        weight = format_japanese_number(player.weight) + " kg" if player.weight else '不明'

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
            'team_logo': team_logo,
            'number': number,
            'position': player.main_position_category,
            'birthday': player.birthday,
            'age': player.age,
            'throw_bat_display': player.throw_bat_display,
            'height': height,
            'weight': weight,
            'place': player.place,
            'salary': salary,
            'color': team_color,
        })

    return render(request, 'players/player_list.html', {'players': player_data})