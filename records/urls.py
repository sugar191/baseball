from django.urls import path
from . import views

urlpatterns = [
    path("records/<int:year>/", views.salaries, name="salaries"),
]
