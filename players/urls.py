from django.urls import path
from . import views

urlpatterns = [
    path('players/', views.player_list, name='player_list'),
    path('players/add/', views.add_player, name='add_player'),  # 選手追加
]