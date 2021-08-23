from django.db.models import Q
from django.shortcuts import render, redirect
from .models import League, Team, Player

from . import team_maker

league_filters = {
                   'all':           League.objects.all(),
                   'women':         League.objects.filter(name__contains='women'),
                   'hockey':        League.objects.filter(sport__contains='hockey'),
                   'not_football':  League.objects.exclude(sport__contains='football'),
                   'conferences':   League.objects.filter(name__contains='conference'),
                   'atlantic':      League.objects.filter(name__contains='atlantic')
        }


team_filters = {
                 'sortalph':    Team.objects.all().order_by('team_name'),
                 'sortralph':   Team.objects.all().order_by('-team_name'),
                 'sortloc':     Team.objects.all().order_by('location'),
                 'dallas':      Team.objects.filter(location__contains='Dallas'),
                 'raptors':     Team.objects.filter(team_name__contains='Raptors'),
                 'city':        Team.objects.filter(location__contains='City'),
                 't':           Team.objects.filter(team_name__startswith='T')
               }


player_filters = {
                   'all':                Player.objects.all(),
                   'cooper':             Player.objects.filter(last_name='Cooper'),
                   'joshua':             Player.objects.filter(first_name='Joshua'),
                   'cooper_not_joshua':  Player.objects.filter(last_name='Cooper').exclude(first_name='Joshua'),
                   'alexander_or_wyatt': Player.objects.filter(Q(first_name='Alexander')|Q(first_name='Wyatt'))
                 }


def index(request):
    if 'league_filter' in request.POST:
        leagues = league_filters[request.POST['league_filter']]
    else:
        leagues = League.objects.all()

    if 'teams_filter' in request.POST:
        teams = team_filters[request.POST['teams_filter']]
    else:
        teams = Team.objects.all().order_by('team_name')

    if 'players_filter' in request.POST:
        players = player_filters[request.POST['players_filter']]
    else:
        players = player_filters['all']

    context = {
		"leagues": leagues,
		"teams":   teams,
		"players": players
	}
    return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")
