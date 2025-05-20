from django.shortcuts import render
from .models import PlayerSalaryView


# Create your views here.
def salaries(request, year):
    salaries = PlayerSalaryView.objects.filter(year=year).order_by("-salary")

    return render(
        request,
        "records/salaries.html",
        {
            "salaries": salaries,
            "year": year,
        },
    )
