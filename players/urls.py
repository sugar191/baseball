from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('players/', views.player_list, name='player_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)