# views.py
from django.shortcuts import render
from .models import Fixture

def FixtureList(request):
    # Get all fixtures and order them by round number
    fixtures = Fixture.objects.all().order_by('round_number')

    # Group fixtures by round number
    fixtures_by_round = {}
    for fixture in fixtures:
        if fixture.round_number not in fixtures_by_round:
            fixtures_by_round[fixture.round_number] = []
        fixtures_by_round[fixture.round_number].append(fixture)

    return render(request, 'league/League_Matches.html', {'fixtures_by_round': fixtures_by_round})


def TeamMatches(request):
    team_fixtures = None  # Initialize team_fixtures to None
    if request.method == 'GET':
        team_name = request.GET.get('team_name', None)
        if team_name:
            # Fetch all fixtures where the provided team is either the home team or away team
            team_fixtures = Fixture.objects.filter(home_team__icontains=team_name) |  Fixture.objects.filter(away_team__icontains=team_name)
    return render(request, template_name='league/Team_Matches.html', context={'team_fixtures': team_fixtures})



from django.shortcuts import render
from .models import Fixture
from datetime import date

def team_manager_dashboard(request):
    # Welcome message
    user = request.user
    welcome_message = f"Welcome {user} to Team Manager Dashboard!"

    # Fetching all fixtures
    all_fixtures = Fixture.objects.all()

    # Filtering user's team fixtures
    user_team_fixtures = Fixture.objects.filter(home_team=user) | Fixture.objects.filter(away_team=user)

    # Filtering played and non-played fixtures
    today = date.today()
    played_fixtures = Fixture.objects.filter(match_date__lt=today)
    non_played_fixtures = Fixture.objects.filter(match_date__gte=today)

    # Next 5 matches
    next_matches = Fixture.objects.filter(match_date__gte=today).order_by('match_date')[:5]

    # Previous 5 matches
    previous_matches = Fixture.objects.filter(match_date__lt=today).order_by('-match_date')[:5]

    context = {
        'welcome_message': welcome_message,
        'all_fixtures': all_fixtures,
        'user_team_fixtures': user_team_fixtures,
        'played_fixtures': played_fixtures,
        'non_played_fixtures': non_played_fixtures,
        'next_matches': next_matches,
        'previous_matches': previous_matches,
    }

    return render(request, 'league/TeamManager.html', context)
