from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import User,Team
from django.contrib import admin
from league.models import  Fixture
from users.models import Team
from rule.models import Rule
from league.fixture import generate_double_round_robin_fixtures
from league.AIFixture import generate_data_mined_fixtures,load_historical_data
from league.AIFixture import load_historical_data, count_team_appearances_across_years
from django.shortcuts import render
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email','first_name','last_name','phoneNo','team']
    list_display = ['email','first_name','last_name','phoneNo','team','is_active']
    
    readonly_fields=["userimage"]
    def userimage(self, obj):
        if obj.userImage:
            return mark_safe(f'<img src="{obj.userImage.url}" width="100" height="100" />')
        return "No Image"


class TeamStatusFilter(admin.SimpleListFilter):
    title = 'Team Status'
    parameter_name = 'team_status'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active'),
            ('relegate', 'Relegate'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(TeamStatus='active')
        elif self.value() == 'relegate':
            return queryset.filter(TeamStatus='relegate')
        return queryset





class TeamAdmin(admin.ModelAdmin):
    actions = ['generate_fixtures','generate_fixture','display_team_statistics']
    search_fields = ['TeamName', 'TeamStadium', 'TeamCity']
    list_display = ['TeamName', 'TeamStadium', 'TeamCity', 'TeamStatus']
    list_filter = [TeamStatusFilter]

    def display_team_statistics(self, request, queryset):
        historical_data = load_historical_data()
        team_years_count = count_team_appearances_across_years(historical_data)
        context = {'team_years_count': team_years_count}
        return render(request, 'admin/team_statistics.html', context)

    display_team_statistics.short_description = "Display Team Appearance Statistics"
    
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
        modeladmin.message_user(request, "Your fixtures are Successfully generated.")

    generate_fixtures.short_description = "Generate fixtures normal"
    
    # FOR DATAMINING
    def generate_fixture(modeladmin, request, queryset):
        teams = queryset.all()
        rules = {rule.name: rule.value for rule in Rule.objects.all()}
        historical_data = load_historical_data()
        fixtures, start_date = generate_data_mined_fixtures(teams, rules, historical_data)

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
        modeladmin.message_user(request, "Your fixtures are Successfully generated.")

    generate_fixture.short_description = "Generate fixtures by History"



admin.site.register(User,UserAdmin)
admin.site.register(Team,TeamAdmin)


