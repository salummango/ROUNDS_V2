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

def generate_fixtures(modeladmin, request, queryset):
    teams = queryset.all()
    rules = {rule.name: rule.value for rule in Rule.objects.all()}
    fixtures, start_date = generate_double_round_robin_fixtures(teams, rules)

    for round_num, round_matches in enumerate(fixtures, start=1):
        for match in round_matches:
            home_team, away_team,  match_date = match
            
            # Determine the stadium and city for the fixture
            match_stadium = home_team.TeamStadium  # assign each team with it's stadium
            # match_city = home_team.city  # assign each team with it's city
            
            #assigning logos for team to be used on calendar
            home_logo=home_team.TeamLogo
            away_logo=away_team.TeamLogo
            
            fixture = Fixture(
                home_team=home_team,
                away_team=away_team,
                match_date=match_date,
                round_number=round_num,  
                match_stadium=match_stadium,
                # match_city=match_city,
                home_logo=home_logo,
                away_logo=away_logo,
                
            )
            fixture.save()


generate_fixtures.short_description = "Generate fixtures"


   

class FixtureResource(resources.ModelResource):#This class specifies the model to be used for importing and exporting data.
    class Meta:
        model = Fixture

class FixtureAdmin(ImportExportModelAdmin):
    resource_class = FixtureResource
    search_fields = ['home_team', 'away_team', 'match_date','match_stadium']
    list_display = ['round_number', 'id',  'home_team', 'away_team', 'match_date','match_stadium']
    ordering = ['round_number', 'id']


admin.site.register(Fixture,FixtureAdmin)


