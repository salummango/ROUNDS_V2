# views.py

from django.core.exceptions import ValidationError
from django.utils.html import escape

def TeamMatches(request):
    team_fixtures = None  # Initialize team_fixtures to None
    if request.method == 'GET':
        team_name = request.GET.get('team_name', None)
        if team_name:
            # Escape any special characters in the team name to prevent XSS
            team_name = escape(team_name)
            # Fetch all fixtures where the provided team is either the home team or away team
            try:
                team_fixtures = Fixture.objects.filter(home_team__icontains=team_name) | Fixture.objects.filter(away_team__icontains=team_name)
            except ValidationError:
                team_fixtures = None  # Handle the case where the query could not be processed
    return render(request, template_name='league/Team_Matches.html', context={'team_fixtures': team_fixtures})


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Fixture
from datetime import date, datetime
from calendar import HTMLCalendar, monthcalendar
from users.models import User, Team
from django.db.models import Count
from matplotlib import pyplot as plt
from django.conf import settings
import os


from django.core.exceptions import PermissionDenied
from Letter.models import Letter
from Letter.forms import LetterForm
from django.core.paginator import Paginator
@login_required(login_url='/api/login/')
def team_manager_dashboard(request):
    user_team = request.user.team

    # Fetch all fixtures and order them by round number
    all_fixtures = Fixture.objects.all().order_by('round_number')
    
    


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

    if request.method == 'POST':
        form = LetterForm(request.POST, user=request.user)
        if form.is_valid():
            letter = form.save(commit=False)
            letter.sender = request.user
            letter.save()
            return redirect('team_manager_dashboard')  # Redirect to inbox view or a success page
    else:
        form = LetterForm(user=request.user)
    
    received_letters = Letter.objects.filter(receiver=request.user)
    sent_letters = Letter.objects.filter(sender=request.user)
    
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
        'form': form,
        
        'received_letters':received_letters,
        'sent_letters':sent_letters,
        
    }

    return render(request, 'managerdashboard.html', context)



