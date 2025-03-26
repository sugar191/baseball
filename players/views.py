from django.shortcuts import render
from .models import Player, PlayerCommonRecord

# 選手一覧を表示するビュー
def player_list(request):
    players = Player.objects.all()  # Playerモデルから全ての選手を取得

    player_data = []
    for player in players:
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
            'age': player.age,
            'throw_bat_display': player.throw_bat_display,
        })

    return render(request, 'players/player_list.html', {'players': player_data})