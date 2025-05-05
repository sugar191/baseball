from django.shortcuts import render
from django.db.models import Q
from .models import Team, Organization

# 選手一覧を表示するビュー
def team_list(request):
    qs = Team.objects.all()

    organization_id = request.GET.get('organization', '')
    organizations = Organization.objects.all()

    filters = Q()  # 初期化
    if organization_id:
        filters &= Q(league__organization_id=organization_id)

    teams = qs.filter(filters)

    return render(request, 'teams/team_list.html', {
        'teams': teams,
        'organizations': organizations,
    })
