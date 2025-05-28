from django.shortcuts import render, get_object_or_404, redirect
from .forms import (
    PlayerForm,
    PlayerCommonRecordFormSet,
    GameForm,
    TransferForm,
    TeamSeasonEditForm,
)
from players.models import Player
from games.models import Game
from transfers.models import Transfer
from teams.models import TeamSeason
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory


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

            # 元の検索条件に戻す
            next_url = request.GET.get(
                "next", request.META.get("HTTP_REFERER", "/games/")
            )
            return redirect(next_url)
    else:
        form = GameForm(instance=game)

    return render(
        request,
        "admin_panel/game_edit.html",
        {"form": form, "game": game},
    )


@login_required
@user_passes_test(staff_check)
def transfer_edit(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("transfer_edit")
    else:
        form = TransferForm()
        transfers = Transfer.objects.all()

    return render(
        request,
        "admin_panel/transfer_edit.html",
        {"form": form, "transfers": transfers},
    )


def team_season_edit(request):
    TeamSeasonFormSet = modelformset_factory(
        TeamSeason, form=TeamSeasonEditForm, extra=0
    )
    queryset = TeamSeason.objects.all().order_by(
        "team__league__sort_order", "sort_order"
    )

    if request.method == "POST":
        formset = TeamSeasonFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            return redirect("top_page")
        else:
            for form in formset:
                print(form.errors)
    else:
        formset = TeamSeasonFormSet(queryset=queryset)

    return render(request, "admin_panel/team_season_edit.html", {"formset": formset})
