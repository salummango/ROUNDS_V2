# Assuming you have already implemented count_team_appearances_across_years function
from django.conf import settings
import os
import matplotlib.pyplot as plt
from .AIFixture import count_team_appearances_across_years, load_historical_data

def generate_team_appearances_chart():
    # Load historical data and count team appearances
    historical_data = load_historical_data()
    team_years_count = count_team_appearances_across_years(historical_data)

    # Extract teams and counts
    teams = list(team_years_count.keys())
    appearances = list(team_years_count.values())

    # Plotting the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(teams, appearances, color='skyblue')
    plt.xlabel('Teams')
    plt.ylabel('Number of Appearances')
    plt.title('Team Appearances Across Years')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot as an image file
    image_path = os.path.join(settings.MEDIA_ROOT, 'charts', 'team_appearances_chart.png')
    plt.savefig(image_path)

    return image_path
