from django.urls import path
from . import views

urlpatterns = [
    path('drafts/', views.draft_list, name='draft_list'),
    path('drafts/<int:year>/', views.draft_detail, name='draft_detail'),
]