from django.shortcuts import render
from .models import Player, PlayerCommonRecord

# 選手一覧を表示するビュー
def player_list(request):
    players = Player.objects.all()  # Playerモデルから全ての選手を取得

    player_data = []
    for player in players:
        # 数値をフォーマット
        if player.height is not None:
            # 小数点以下が0なら整数として、そうでなければそのまま
            if player.height == int(player.height):
                player.formatted_height = int(player.height)  # 整数にする
            else:
                player.formatted_height = float(player.height)  # floatに変換して余分なゼロを取り除く
        else:
            player.formatted_height = None
        
        if player.weight is not None:
            # 小数点以下が0なら整数として、そうでなければそのまま
            if player.weight == int(player.weight):
                player.formatted_weight = int(player.weight)  # 整数にする
            else:
                player.formatted_weight = float(player.weight)  # floatに変換して余分なゼロを取り除く
        else:
            player.formatted_weight = None

        # 最新年度のレコードを取得
        latest_record = PlayerCommonRecord.objects.filter(player=player).order_by('-year').first()
        name = latest_record.registered_name if latest_record else None
        team_logo = latest_record.team.logo if latest_record else None
        number = latest_record.number if latest_record else None

        player_data.append({
            'id': player.id,
            'name': name,
            'team_logo': team_logo,
            'number': number,
            'position': player.main_position_category,
            'birthday': player.birthday,
            'age': player.age,
            'throw_bat_display': player.throw_bat_display,
            'height': player.formatted_height,
            'weight': player.formatted_weight,
            'place': player.place,
        })

    return render(request, 'players/player_list.html', {'players': player_data})