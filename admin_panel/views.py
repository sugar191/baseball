from django.shortcuts import render, get_object_or_404, redirect
from .forms import PlayerForm, PlayerCommonRecordFormSet, GameForm
from players.models import Player
from games.models import Game
from django.contrib.auth.decorators import login_required, user_passes_test


def staff_check(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(staff_check)
def player_edit(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == "POST":
        form = PlayerForm(request.POST, instance=player)
        common_record_formset = PlayerCommonRecordFormSet(request.POST, instance=player)
        if form.is_valid() and common_record_formset.is_valid():
            form.save()
            common_record_formset.save()
            return redirect(
                "player_detail", player_id=player.pk
            )  # 詳細ページへリダイレクト
    else:
        form = PlayerForm(instance=player)
        common_record_formset = PlayerCommonRecordFormSet(instance=player)

    return render(
        request,
        "admin_panel/player_edit.html",
        {"form": form, "formset": common_record_formset, "player": player},
    )


@login_required
@user_passes_test(staff_check)
def game_edit(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == "POST":
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect("games", pk=game.pk)  # 適切なリダイレクト先に変更
        else:
            form = GameForm(instance=game)

    return render(
        request,
        "admin_panel/game_edit.html",
        {"form": form, "game": game},
    )
