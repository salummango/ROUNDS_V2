# admin.py
from django.contrib import admin
from .models import  Fixture
from users.models import Team
from rule.models import Rule
from .fixture import generate_double_round_robin_fixtures
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from datetime import datetime
from django.utils import timezone
# from .AIFixture import generate_data_mined_fixtures,load_historical_data

# def generate_fixtures(modeladmin, request, queryset):
#     teams = queryset.all()
#     rules = {rule.name: rule.value for rule in Rule.objects.all()}
#     fixtures, start_date = generate_double_round_robin_fixtures(teams, rules)

#     for round_num, round_matches in enumerate(fixtures, start=1):
#         for match in round_matches:
#             home_team, away_team,  match_date = match
            
#             # Determine the stadium and city for the fixture
#             match_stadium = home_team.TeamStadium  # assign each team with it's stadium
#             # match_city = home_team.city  # assign each team with it's city
            
#             #assigning logos for team to be used on calendar
#             home_logo=home_team.TeamLogo
#             away_logo=away_team.TeamLogo
            
#             fixture = Fixture(
#                 home_team=home_team,
#                 away_team=away_team,
#                 match_date=match_date,
#                 round_number=round_num,  
#                 match_stadium=match_stadium,
#                 # match_city=match_city,
#                 home_logo=home_logo,
#                 away_logo=away_logo,
                
#             )
#             fixture.save()
#     modeladmin.message_user(request, "Your fixtures are Successfully generated.")


# generate_fixtures.short_description = "Generate fixtures normal"

# # FOR DATAMINING
# def generate_fixture(modeladmin, request, queryset):
#     teams = queryset.all()
#     rules = {rule.name: rule.value for rule in Rule.objects.all()}
#     historical_data = load_historical_data()
#     fixtures, start_date = generate_data_mined_fixtures(teams, rules, historical_data)

#     for round_num, round_matches in enumerate(fixtures, start=1):
#         for match in round_matches:
#             home_team, away_team,  match_date = match
            
#             # Determine the stadium and city for the fixture
#             match_stadium = home_team.TeamStadium  # assign each team with it's stadium
#             # match_city = home_team.city  # assign each team with it's city
            
#             #assigning logos for team to be used on calendar
#             home_logo=home_team.TeamLogo
#             away_logo=away_team.TeamLogo
            
#             fixture = Fixture(
#                 home_team=home_team,
#                 away_team=away_team,
#                 match_date=match_date,
#                 round_number=round_num,  
#                 match_stadium=match_stadium,
#                 # match_city=match_city,
#                 home_logo=home_logo,
#                 away_logo=away_logo,
                
#             )
#             fixture.save()
#     modeladmin.message_user(request, "Your fixtures are Successfully generated.")


# generate_fixture.short_description = "Generate fixtures by History"

# from league.AIFixture import load_historical_data, count_team_appearances_across_years
# from django.shortcuts import render
# def display_team_statistics(self, request, queryset):
#         historical_data = load_historical_data()
#         team_years_count = count_team_appearances_across_years(historical_data)
#         context = {'team_years_count': team_years_count}
#         return render(request, 'admin/team_statistics.html', context)

# display_team_statistics.short_description = "Display Team Appearance Statistics"
    
import os
import csv
from django.conf import settings
from .models import Fixture
from LeagueHistory.models import HistoricalFixtureFile

def export_fixtures_to_history(modeladmin, request, queryset):
    # Determine the earliest and latest years in the selected fixtures
    years = queryset.dates('match_date', 'year')
    if not years:
        modeladmin.message_user(request, "No fixtures selected.", level='error')
        return
    
    start_year = years[0].year
    end_year = years[len(years) - 1].year

    csv_filename = os.path.join(settings.MEDIA_ROOT, 'historical_fixtures', f'fixtures_{start_year}_{end_year}.csv')
    os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['home_team', 'away_team', 'match_date', 'round_number', 'match_stadium'])
        for fixture in queryset:
            writer.writerow([fixture.home_team, fixture.away_team, fixture.match_date, fixture.round_number, fixture.match_stadium])

    # Save the file reference in HistoricalFixtureFile model
    HistoricalFixtureFile.objects.create(file=f'historical_fixtures/fixtures_{start_year}_{end_year}.csv')

    modeladmin.message_user(request, "Successfully exported fixtures to history.")

export_fixtures_to_history.short_description = "Export selected fixtures to history"




class FixtureResource(resources.ModelResource):#This class specifies the model to be used for importing and exporting data.
    class Meta:
        model = Fixture

class FixtureAdmin(ImportExportModelAdmin):
    resource_class = FixtureResource
    search_fields = ['home_team', 'away_team', 'match_date','match_stadium']
    list_display = ['round_number', 'id',  'home_team', 'away_team', 'match_date','match_stadium']
    ordering = ['round_number', 'id']
    actions = [export_fixtures_to_history]


admin.site.register(Fixture,FixtureAdmin)


