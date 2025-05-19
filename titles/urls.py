from django.urls import path
from . import views

urlpatterns = [
    path("titles/", views.title_list, name="title_list"),
    path("titles/<int:title_id>/", views.title_detail, name="title_detail"),
]
