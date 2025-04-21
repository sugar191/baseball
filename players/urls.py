from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('players/', views.player_list, name='player_list'),
    path('players/<int:player_id>/', views.player_detail, name='player_detail'),
    path('players/<int:player_id>/<int:year>/', views.player_year_detail, name='player_year_detail'),
    path('players/<int:pk>/edit/', views.player_edit, name='player_edit'),
]