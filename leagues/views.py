from django.db.models import Q, Count
from django.shortcuts import render, redirect
from .models import League, Team, Player

from . import team_maker

league_filters = {
        'all':           { 
                           'description': 'All Leagues',
                           'filter':      League.objects.all()
                         },
        'women':         { 
                            'description': 'All Women Leagues',
                            'filter':      League.objects.filter(name__contains='women')
                         },
        'hockey':        {
                           'description':  'All Hockey Leagues',
                           'filter':       League.objects.filter(sport__contains='hockey')
                         },
        'not_football':  {
                           'description':  'All Non-Football Leagues',
                           'filter':       League.objects.exclude(sport__contains='football')
                         },
        'conferences':   {
                           'description':  'All conferences',
                           'filter':       League.objects.filter(name__contains='conference')
                         },
        'atlantic':      {
                           'description':  'All Atlantic leagues',
                           'filter':       League.objects.filter(name__contains='atlantic')
                         },
        'sophia':        {
                           'description': 'All leagues with a current player named "Sophia"',
                           'filter':      League.objects.filter(Q(teams__curr_players__first_name='Sophia') |
                                                                Q(teams__curr_players__last_name='Sophia'))
                         }
        }


team_filters = {
        'all':          { 
                          'description': 'All Teams, Sorted by Alphabetical Order',
                          'filter':      Team.objects.all().order_by('team_name')
                        },
        'sortralph':    {
                          'description': 'All Teams, Sorted by Reverse Alphabetical Order',
                          'filter':      Team.objects.all().order_by('-team_name')
                        },
        'sortloc':      {
                          'description': 'All Teams, Sorted by Location',
                          'filter':      Team.objects.all().order_by('location')
                        },
        'dallas':       {
                          'description': 'All Dallas Teams',
                          'filter':      Team.objects.filter(location__contains='Dallas')
                        },
        'raptors':      { 'description': 'All "Raptor" Teams',
                          'filter':      Team.objects.filter(team_name__contains='Raptors')
                        },
        'city':         { 
                          'description': 'All "City" Teams',
                          'filter':      Team.objects.filter(location__contains='City')
                        },
        't':            {
                          'description': 'All Team Names Beginning With "T"',
                          'filter':      Team.objects.filter(team_name__startswith='T')
                        },
        'atlantic':     {
                          'description': 'All teams in the Atlantic Soccer Conference',
                          'filter':      Team.objects.filter(Q(league__name__contains='Atlantic') &
                                                             Q(league__sport__contains='Soccer'))
                        },
        'sophia':       {
                          'description': 'All teams with a current player named "Sophia"',
                          'filter':      Team.objects.filter(Q(curr_players__first_name='Sophia') |
                                                             Q(curr_players__last_name='Sophia'))
                        },
        'samuel_evans': {
                          'description': 'All teams (past & present) that Samuel Evans has played with',
                          'filter':      Team.objects.filter(Q(all_players__first_name='Samuel') &
                                                             Q(all_players__last_name='Evans'))
                        },
        'gray_before_colts': {
                               'description': 'Every team that Jacob Gray played for before he joined the Oregon Colts',
                               'filter':      Team.objects.filter(Q(all_players__first_name='Jacob') &
                                                                  Q(all_players__last_name='Gray')
                                                        ).exclude(Q(team_name='Colts') &
                                                                  Q(location='Oregon'))
                             },
        '12_plus_players':   {
                               'description': 'All teams that have had 12 or more players, past and present',
                               'filter':      Team.objects.annotate(num_total_players=Count('all_players')).filter(num_total_players__gte=12)
                             }
               }


player_filters = {
                   'all':                    { 
                                               'description': 'All players',
                                               'filter':      Player.objects.all()
                                             },
                   'cooper':                 {
                                               'description': 'All players with last name Cooper',
                                               'filter':      Player.objects.filter(last_name='Cooper')
                                             },
                   'joshua':                 {
                                               'description': 'All players with first name Joshua',
                                               'filter':      Player.objects.filter(first_name='Joshua')
                                             },
                   'cooper_not_joshua':      {
                                               'description': 'All players with last name Cooper except those with Joshua as first name',
                                               'filter':      Player.objects.filter(last_name='Cooper').exclude(first_name='Joshua')
                                             },
                   'alexander_or_wyatt':     {
                                               'description': 'All players with first name Alexander -or- Wyatt',
                                               'filter':      Player.objects.filter(Q(first_name='Alexander') |
                                                                                    Q(first_name='Wyatt'))
                                             },
                   'boston_penguins':        {
                                               'description': 'All current players on the Boston Penguins',
                                               'filter':      Player.objects.filter(Q(curr_team__team_name__contains='Penguins') &
                                                                                    Q(curr_team__location__contains='Boston'))
                                             },
                   'int_coll_baseball':      {
                                               'description': 'All current players in the International Collegiate Baseball Conference',
                                               'filter':      Player.objects.filter(Q(curr_team__league__name__contains='International Collegiate') &
                                                                                    Q(curr_team__league__sport__contains='Baseball'))
                                             },
                   'acaf_lopez':             {
                                               'description': 'All current players in the American Conference of Amateur Football with the last name of Lopez',
                                               'filter':      Player.objects.filter(Q(last_name='Lopez') &
                                                                                    Q(curr_team__league__name__contains='American Conference of Amateur Football'))
                                             },
                   'football':               {
                                               'description': 'All football players',
                                               'filter':      Player.objects.filter(curr_team__league__sport__contains='Football')
                                             },
                   'flores_not_roughriders': {
                                               'description': 'Everyone with the last name "Flores" who DOESN\'T currently play for the Washington Roughriders',
                                               'filter':       Player.objects.filter(last_name='Flores').exclude(Q(curr_team__location='Washington') &
                                                                                                                 Q(curr_team__team_name='Roughriders'))
                                             },
                   'mb_tigercats':           {
                                               'description': 'All players, past and present, with the Manitoba Tiger-Cats',
                                               'filter':      Player.objects.filter(Q(all_teams__team_name='Tiger-Cats') &
                                                                                    Q(all_teams__location='Manitoba'))
                                             },
                   'former_wichita_vikings': {
                                               'description': 'All players who were formerly (but aren\'t currently) with the Wichita Vikings',
                                               'filter':      Player.objects.exclude(Q(curr_team__team_name='Vikings') &
                                                                                     Q(curr_team__location='Wichita')
                                                                            ).filter(Q(all_teams__team_name='Vikings') &
                                                                                     Q(all_teams__location='Wichita'))
                                             },
                   'joshua_afabp':           {
                                               'description': 'Everyone named "Joshua" who has ever played in the Atlantic Federation of Amateur Baseball Players',
                                               'filter':      Player.objects.filter(Q(first_name='Joshua') &
                                                                                    Q(all_teams__league__name='Atlantic Federation of Amateur Baseball Players'))
                                             },
                  'all_teams_count':         {
                                               'description': 'All players and count of teams played for, sorted by the number of teams they\'ve played for',
                                               'filter':      Player.objects.annotate(teams_played_for=Count('all_teams')).order_by('-teams_played_for')
                                             }
                 }


def index(request):
    if 'league_filter' in request.POST:
        league_filter = request.POST['league_filter']
    else:
        league_filter = 'all'
    leagues = league_filters[league_filter]['filter']

    if 'teams_filter' in request.POST:
        teams_filter = request.POST['teams_filter']
    else:
        teams_filter = 'all'
    teams = team_filters[teams_filter]['filter']

    if 'players_filter' in request.POST:
        players_filter = request.POST['players_filter']
    else:
        players_filter = 'all'
    players = player_filters[players_filter]['filter']
    
    context = {
		'leagues':             league_filters[league_filter]['filter'],
		'teams':               team_filters[teams_filter]['filter'],
		'players':             player_filters[players_filter]['filter'],
        'league_filters':      league_filters,
        'team_filters':        team_filters,
        'player_filters':      player_filters,
        'curr_league_filter':  league_filter,
        'curr_teams_filter':   teams_filter,
        'curr_players_filter': players_filter
	}
    return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")
