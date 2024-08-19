import csv
import os
import json
import ast
import random
from datetime import datetime, timedelta
from collections import defaultdict
from dateutil.parser import parse
from rule.models import Rule
from users.models import Team
from LeagueHistory.models import HistoricalFixtureFile
from django.conf import settings

def load_rules_from_database():
    """Load rules from the database."""
    rules = Rule.objects.all()
    return {rule.name: rule.value for rule in rules}

def load_historical_data():
    """Load historical fixture data from CSV files."""
    historical_data = []
    files = HistoricalFixtureFile.objects.all()
    for file_record in files:
        file_path = os.path.join(settings.MEDIA_ROOT, file_record.file.name)
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                historical_data.append(row)
    return historical_data

def analyze_historical_patterns(historical_data):
    """Analyze historical data to find patterns."""
    day_frequency = defaultdict(int)
    time_frequency = defaultdict(lambda: defaultdict(int))
    past_first_matches = defaultdict(lambda: defaultdict(set))
    
    for row in historical_data:
        match_date = parse(row['match_date'])  # Using dateutil.parser.parse to handle timezone
        day_of_week = match_date.strftime('%A')
        time_of_day = match_date.strftime('%H:%M')
        year = match_date.year
        day_frequency[day_of_week] += 1
        time_frequency[row['home_team']][time_of_day] += 1
        time_frequency[row['away_team']][time_of_day] += 1

        # Track the first match of each team for each year
        if row['round_number'] == '1':  # Assuming 'round_number' is available in the CSV
            past_first_matches[year][row['home_team']].add(row['away_team'])
            past_first_matches[year][row['away_team']].add(row['home_team'])
    
    return day_frequency, time_frequency, past_first_matches

def generate_data_mined_fixtures(teams, rules, historical_data):
    """Generate fixtures based on historical data mining."""
    num_teams = len(teams)
    num_rounds = 2 * (num_teams - 1)
    matches = []

    start_date_str = rules['LeagueStartDate']
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

    
    fifa_calendar_str = rules.get('FIFACALENDAR', '[]')
    fifa_calendar = json.loads(fifa_calendar_str)

    weekend_rule_str = rules['WeekendScheduling']
    try:
        weekend_rule = json.loads(weekend_rule_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        weekend_rule = {}

    if isinstance(weekend_rule, dict):
        total_match_days_per_week = sum(weekend_rule.values())
    else:
        total_teams = len(teams)
        total_match_days_per_week = total_teams // 2

    rotation_index = 0

    stadiums = defaultdict(list)
    cities = defaultdict(list)
    for team in teams:
        stadiums[team.TeamStadium].append(team)
        cities[team.TeamCity].append(team)

    day_frequency, time_frequency, past_first_matches = analyze_historical_patterns(historical_data)

    current_year = start_date.year

    for i in range(num_rounds):
        round_matches = []

        half = num_teams // 2
        first_half = teams[:half]
        second_half = teams[half:]

        current_week_match_days = 0

        for j in range(half):
            if i % 2 == 0:
                home_team, away_team = first_half[j], second_half[-(j + 1)]
            else:
                home_team, away_team = second_half[-(j + 1)], first_half[j]

            # Check for duplicate first matches from the past year
            if j == 0:  # Check for the first match of each team
                while (away_team.TeamName in past_first_matches[current_year - 1][home_team.TeamName] or 
                       home_team.TeamName in past_first_matches[current_year - 1][away_team.TeamName]):
                    teams = teams[1:] + teams[:1]  # Rotate teams to avoid duplicate first matches
                    first_half = teams[:half]
                    second_half = teams[half:]
                    if i % 2 == 0:
                        home_team, away_team = first_half[j], second_half[-(j + 1)]
                    else:
                        home_team, away_team = second_half[-(j + 1)], first_half[j]

            while current_week_match_days == 0:
                match_date = start_date + timedelta(days=rotation_index)
                for event in fifa_calendar:
                    if event['start_date'] == '0000-00-00' and event['end_date'] == '0000-00-00':
                        continue  # Skip invalid date entries
                    start_date_obj = datetime.strptime(event['start_date'], '%Y-%m-%d').date()
                    end_date_obj = datetime.strptime(event['end_date'], '%Y-%m-%d').date()
                    if start_date_obj <= match_date.date() <= end_date_obj:
                        rotation_index += 1
                        match_date = start_date + timedelta(days=rotation_index)
                        break
                else:
                    current_week_match_days = weekend_rule.get(match_date.strftime('%A'), 0)
                    rotation_index += 1

            if home_team.TeamStadium == away_team.TeamStadium:
                rotation_index += 1
                match_date = start_date + timedelta(days=rotation_index)

            if len(cities[home_team.TeamCity]) > 2:
                rotation_index += 1
                match_date = start_date + timedelta(days=rotation_index)

            kick_off_times_str = rules.get('KickOff', '[]')
            kick_off_times = ast.literal_eval(kick_off_times_str)

            if time_frequency[home_team.TeamName]:
                kick_off_time = max(time_frequency[home_team.TeamName], key=time_frequency[home_team.TeamName].get)
            elif time_frequency[away_team.TeamName]:
                kick_off_time = max(time_frequency[away_team.TeamName], key=time_frequency[away_team.TeamName].get)
            else:
                kick_off_time = random.choice(kick_off_times)

            kick_off_time_obj = datetime.strptime(kick_off_time, '%H:%M').time()
            match_date_with_time = datetime.combine(match_date, kick_off_time_obj)
            match_date = match_date_with_time

            round_matches.append((home_team, away_team, match_date))
            current_week_match_days -= 1

        teams = teams[1:] + teams[:1]
        matches.append(round_matches)

    return matches, start_date



# AIFixture.py

from collections import defaultdict, Counter
from datetime import datetime

def count_team_appearances_across_years(historical_data):
    """Count how many years each team has appeared in the fixtures."""
    team_years_count = defaultdict(int)

    years_data = defaultdict(list)

    # Group fixtures by year
    for fixture in historical_data:
        match_date = datetime.strptime(fixture['match_date'], '%Y-%m-%d %H:%M:%S%z')
        year = match_date.year
        years_data[year].append(fixture)

    for year, fixtures in years_data.items():
        teams_in_year = set()
        for fixture in fixtures:
            teams_in_year.add(fixture['home_team'])
            teams_in_year.add(fixture['away_team'])

        for team in teams_in_year:
            team_years_count[team] += 1

    # Convert defaultdict to regular dictionary
    team_years_count = dict(team_years_count)

    return team_years_count


