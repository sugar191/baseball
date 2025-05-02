from django.urls import path
from . import views

urlpatterns = [
    path('players/<int:player_id>/edit/', views.player_edit, name='player_edit'),
]