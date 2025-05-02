from django.shortcuts import render, get_object_or_404, redirect
from .forms import PlayerForm, PlayerCommonRecordFormSet
from players.models import Player
from django.contrib.auth.decorators import login_required, user_passes_test

def staff_check(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(staff_check)
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

    return render(request, 'admin_panel/player_edit.html', {
        'form': form,
        'formset': common_record_formset,
        'player': player
    })