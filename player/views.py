from django.shortcuts import render
from .models import Player

def player_list(request):
    players = Player.objects.all()  # 全選手のデータを取得
    return render(request, 'player/player_list.html', {'players': players})