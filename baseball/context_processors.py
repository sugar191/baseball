from careers.models import Career
from teams.models import Team
from places.models import Place
from positions.models import PositionCategory
from players.models import HandBatting, HandThrowing, PlayerCategory


def teams(request):
    teams = Team.objects.filter(is_select=True)
    return {"teams": teams}


def places(request):
    places = Place.objects.all()
    return {"places": places}


def position_categories(request):
    position_categories = PositionCategory.objects.all()
    return {"position_categories": position_categories}


def careers(request):
    careers = Career.objects.all()
    return {"careers": careers}


def throwings(request):
    throwings = HandThrowing.objects.all()
    return {"throwings": throwings}


def battings(request):
    battings = HandBatting.objects.all()
    return {"battings": battings}


def player_categories(request):
    player_categories = PlayerCategory.objects.all()
    return {"player_categories": player_categories}
