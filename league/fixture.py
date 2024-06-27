from datetime import datetime, timedelta
from collections import defaultdict
import ast  # Import the ast module for safely parsing string literals to Python objects
import random
import json
from rule.models import Rule
from users.models import Team

def load_rules_from_database():
    """Load rules from the database."""
    rules = Rule.objects.all()
    return {rule.name: rule.value for rule in rules}

def generate_double_round_robin_fixtures(teams, rules):
    num_teams = len(teams)
    num_rounds = 2 * (num_teams - 1)
    matches = []

    start_date_str = rules['LeagueStartDate']
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

    fifa_calendar = rules.get('FIFACALENDAR', [])  # Get the FIFA calendar from the rules

    # Deserialize JSON string to dictionary
    weekend_rule_str = rules['WeekendScheduling']
    try:
        weekend_rule = json.loads(weekend_rule_str)
    except json.JSONDecodeError as e:
        # Handle the error if the string cannot be parsed
        print(f"Error decoding JSON: {e}")
        weekend_rule = {}

    # Ensure weekend_rule is a dictionary
    if isinstance(weekend_rule, dict):
        total_match_days_per_week = sum(weekend_rule.values())
    else:
        total_teams = len(teams)
        total_match_days_per_week = total_teams // 2  # Handle the case where weekend_rule is not a valid dictionary

    rotation_index = 0

    # Group teams by stadium and city
    stadiums = defaultdict(list)
    cities = defaultdict(list)
    for team in teams:
        stadiums[team.TeamStadium].append(team)
        cities[team.TeamCity].append(team)

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

            while current_week_match_days == 0:
                match_date = start_date + timedelta(days=rotation_index)
                # Check if the match date is in the FIFA calendar, skip if there's an event
                for event in fifa_calendar:
                    if event['start_date'] == '0000-00-00' and event['end_date'] == '0000-00-00':
                        # Skip if no event for the entire month
                        continue
                    start_date_obj = datetime.strptime(event['start_date'], '%Y-%m-%d').date()
                    end_date_obj = datetime.strptime(event['end_date'], '%Y-%m-%d').date()
                    # Check if the match date is in the FIFA calendar, skip if there's an event
                    if start_date_obj <= match_date.date() <= end_date_obj:
                        rotation_index += 1
                        match_date = start_date + timedelta(days=rotation_index)
                        break  # Exit the loop once an event is found for the month
                else:
                    # If no event found for the month, continue with match scheduling
                    current_week_match_days = weekend_rule.get(match_date.strftime('%A'), 0)
                    rotation_index += 1


            # Check StadiumSharing rule
            if home_team.TeamStadium == away_team.TeamStadium:
                # If both teams share the same stadium, move one team's match to the next available day
                rotation_index += 1
                match_date = start_date + timedelta(days=rotation_index)

            # Check SameCity rule
            if len(cities[home_team.TeamCity]) > 2:
                # If the city has more than two teams, move one team's match to the next available day
                rotation_index += 1
                match_date = start_date + timedelta(days=rotation_index)

            # Retrieve kick-off times from the rules and parse it into a list
            kick_off_times_str = rules.get('KickOff', '[]')  # Default to empty list if not found
            
            kick_off_times = ast.literal_eval(kick_off_times_str)  # Parse the string into a list

            # Select a random kick-off time from the list
            kick_off_time = random.choice(kick_off_times)

            # Parse kick_off_time string into a datetime.time object
            kick_off_time_obj = datetime.strptime(kick_off_time, '%H:%M').time()

            # Combine match_date (date object) with kick_off_time_obj (time object)
            match_date_with_time = datetime.combine(match_date, kick_off_time_obj)

            # Assign the combined datetime object to match_date
            match_date = match_date_with_time

            round_matches.append((home_team, away_team, match_date))
            current_week_match_days -= 1

        teams = teams[1:] + teams[:1]
        matches.append(round_matches)

    return matches, start_date

