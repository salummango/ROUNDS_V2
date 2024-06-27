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
from datetime import date, datetime
from calendar import HTMLCalendar, monthcalendar
from users.models import Team
from django.contrib.auth.decorators import login_required

# @login_required
# def team_manager_dashboard(request):
#     if not request.user.is_authenticated:
#         return render(request, 'index.html')  # Redirect to login page if user is not authenticated

#     user_team = request.user.team if request.user.team else None

#     # Fetching all fixtures
#     all_fixtures = Fixture.objects.all()

#     # Filtering user's team fixtures
#     if user_team:
#         user_team_fixtures = Fixture.objects.filter(home_team=user_team) | Fixture.objects.filter(away_team=user_team)
#     else:
#         user_team_fixtures = Fixture.objects.none()  # No fixtures if user has no team

#     # Filtering played and non-played fixtures
#     today = date.today()
#     played_fixtures = Fixture.objects.filter(match_date__lt=today)
#     non_played_fixtures = Fixture.objects.filter(match_date__gte=today)

#     # Next 5 matches
#     next_matches = Fixture.objects.filter(match_date__gte=today).order_by('match_date')[:5]

#     # Previous 5 matches
#     previous_matches = Fixture.objects.filter(match_date__lt=today).order_by('-match_date')[:5]

#     # Fetching all teams
#     teams = Team.objects.all()
#     total_teams = teams.count()
    
#     # for calendar
#     year = int(request.GET.get('year', datetime.today().year))
#     month = int(request.GET.get('month', datetime.today().month))

#     matches = Fixture.objects.filter(match_date__year=year, match_date__month=month)
#     if user_team:
#         user_matches = matches.filter(home_team=user_team) | matches.filter(away_team=user_team)
#     else:
#         user_matches = Fixture.objects.none()

#     calendar = HTMLCalendar()
#     month_calendar = monthcalendar(year, month)

#     # Create a dictionary of match days
#     match_days = {match.match_date.day: [] for match in user_matches}
#     for match in user_matches:
#         match_days[match.match_date.day].append(match)

#     months = [(i, datetime(year, i, 1).strftime('%B')) for i in range(1, 13)]

#     context = {
#         'all_fixtures': all_fixtures,
#         'user_team_fixtures': user_team_fixtures,
#         'played_fixtures': played_fixtures,
#         'non_played_fixtures': non_played_fixtures,
#         'next_matches': next_matches,
#         'previous_matches': previous_matches,
#         'teams': teams,
#         'total_teams': total_teams,
        
#         'year': year,
#         'month': month,
#         'month_calendar': month_calendar,
#         'match_days': match_days,
#         'months': months,
#     }

#     return render(request, 'managerdashboard.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Fixture
from datetime import date, datetime
from calendar import HTMLCalendar, monthcalendar
from users.models import User, Team
from django.db.models import Count
from matplotlib import pyplot as plt
from django.conf import settings
import os
@login_required(login_url='/api/login/')
def team_manager_dashboard(request):
    user_team = request.user.team

    # Fetching all fixtures
    all_fixtures = Fixture.objects.all()

    user_team_fixtures = Fixture.objects.filter(home_team=user_team) | Fixture.objects.filter(away_team=user_team)

    today = date.today()
    played_fixtures = user_team_fixtures.filter(match_date__lt=today)
    non_played_fixtures = user_team_fixtures.filter(match_date__gte=today)

    next_matches = user_team_fixtures.filter(match_date__gte=today).order_by('match_date')[:5]
    previous_matches = user_team_fixtures.filter(match_date__lt=today).order_by('-match_date')[:5]

    teams = Team.objects.all()
    total_teams = teams.count()

    year = int(request.GET.get('year', datetime.today().year))
    month = int(request.GET.get('month', datetime.today().month))

    matches = user_team_fixtures.filter(match_date__year=year, match_date__month=month)
    calendar = HTMLCalendar()
    month_calendar = monthcalendar(year, month)

    match_days = {match.match_date.day: [] for match in matches}
    for match in matches:
        match_days[match.match_date.day].append(match)

    months = [(i, datetime(year, i, 1).strftime('%B')) for i in range(1, 13)]
    
    # statistics
    # Query to get the count of teams per city
    teams_by_city = Team.objects.values('TeamCity').annotate(total_teams=Count('id'))

    # Extracting data for plotting
    cities = [entry['TeamCity'] for entry in teams_by_city]
    total_teams = [entry['total_teams'] for entry in teams_by_city]

    # Plotting the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(cities, total_teams, color='skyblue')
    plt.xlabel('City')
    plt.ylabel('Number of Teams')
    plt.title('Number of Teams per City')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Saving the plot to a file (optional)
    plot_path = os.path.join(settings.MEDIA_ROOT, 'charts', 'teams_by_city_plot.png')
    plt.savefig(plot_path)

    # Plotting the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(total_teams, labels=cities, autopct='%1.1f%%', startangle=140)
    plt.title('Number of Teams per City')
    plt.axis('equal')

    # Save the plot to a file
   
    plot_path_pie = os.path.join(settings.MEDIA_ROOT, 'charts', 'teams_by_city_pie_chart.png')
    plt.savefig(plot_path_pie)
    
    # Retrieve all fixtures
    fixtures = Fixture.objects.all()

    # Dictionaries to store first and last match dates for each team
    first_home_match = {}
    last_home_match = {}
    first_away_match = {}
    last_away_match = {}

    # Process each fixture
    for fixture in fixtures:
        home_team = fixture.home_team
        away_team = fixture.away_team
        match_date = fixture.match_date

        # Update first and last home matches
        if home_team not in first_home_match:
            first_home_match[home_team] = match_date
        last_home_match[home_team] = match_date

        # Update first and last away matches
        if away_team not in first_away_match:
            first_away_match[away_team] = match_date
        last_away_match[away_team] = match_date

    # Identify teams where both the first and last matches are at home
    first_and_last_home_teams = [team for team in first_home_match if first_home_match[team] == last_home_match.get(team)]

    # Identify teams where both the first and last matches are away
    first_and_last_away_teams = [team for team in first_away_match if first_away_match[team] == last_away_match.get(team)]

    # Combine both home and away teams for the third category
    first_and_last_either_teams = list(set(first_and_last_home_teams) | set(first_and_last_away_teams))

    context = {
        'user_team_fixtures': user_team_fixtures,
        'played_fixtures': played_fixtures,
        'non_played_fixtures': non_played_fixtures,
        'next_matches': next_matches,
        'previous_matches': previous_matches,
        'all_fixtures':all_fixtures,
        'teams': teams,
        'total_teams': total_teams,
        'year': year,
        'month': month,
        'month_calendar': month_calendar,
        'match_days': match_days,
        'months': months,
        
        'MEDIA_URL': settings.MEDIA_URL,
        'plot_path': plot_path,  # This should be the relative path within MEDIA_ROOT
        'plot_path_pie':plot_path_pie,
        
        'first_and_last_home_teams': first_and_last_home_teams,
        'first_and_last_away_teams': first_and_last_away_teams,
        'first_and_last_either_teams': first_and_last_either_teams,
    }

    return render(request, 'managerdashboard.html', context)



from calendar import HTMLCalendar, monthcalendar
from datetime import datetime
from django.shortcuts import render
from .models import Fixture

def calendar_view(request):
    year = int(request.GET.get('year', datetime.today().year))
    month = int(request.GET.get('month', datetime.today().month))

    matches = Fixture.objects.filter(match_date__year=year, match_date__month=month)
    calendar = HTMLCalendar()
    month_calendar = monthcalendar(year, month)

    # Create a dictionary of match days
    match_days = {match.match_date.day: [] for match in matches}
    for match in matches:
        match_days[match.match_date.day].append(match)

    months = [(i, datetime(year, i, 1).strftime('%B')) for i in range(1, 13)]

    return render(request, 'calendar.html', {
        'year': year,
        'month': month,
        'month_calendar': month_calendar,
        'match_days': match_days,
        'months': months,
    })


