from django.shortcuts import render, redirect
from .models import Player
from .forms import PlayerForm

# 選手一覧を表示するビュー
def player_list(request):
    players = Player.objects.all()  # Playerモデルから全ての選手を取得
    return render(request, 'players/player_list.html', {'players': players})

# 選手を追加するビュー
def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()  # フォームデータを保存
            return redirect('player_list')  # 登録後に一覧ページへリダイレクト
    else:
        form = PlayerForm()
    return render(request, 'players/add_player.html', {'form': form})