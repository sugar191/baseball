from django.shortcuts import render, get_object_or_404
from .models import Career, PlayerCareerView

# 選手一覧を表示するビュー
def career_list(request):
    careers = Career.objects.all()

    return render(request, 'careers/career_list.html', {
        'careers': careers,
    })

def career_detail(request, career_id):
    career = get_object_or_404(Career, id=career_id)
    players = PlayerCareerView.objects.filter(career_id=career_id).order_by('player_birthday')

    return render(request, 'careers/career_detail.html', {
        'career': career,
        'players': players,
    })