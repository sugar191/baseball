from django.urls import path
from . import views

urlpatterns = [
    path("players/<int:player_id>/edit/", views.player_edit, name="player_edit"),
    path("games/<int:game_id>/edit/", views.game_edit, name="game_edit"),
    path("transfers/edit/", views.transfer_edit, name="transfer_edit"),
    path("team_season_edit/edit/", views.team_season_edit, name="team_season_edit"),
]
