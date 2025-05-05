from django.urls import path
from . import views

urlpatterns = [
    path('careers/', views.career_list, name='career_list'),
    path('careers/<int:career_id>/', views.career_detail, name='career_detail'),
]