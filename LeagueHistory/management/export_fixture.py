from django.core.management.base import BaseCommand
from League.models import Fixture
from LeagueHistory.models import HistoricalFixtureFile
import csv
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Export fixtures from League app to CSV files by year'

    def handle(self, *args, **kwargs):
        fixtures = Fixture.objects.all()

        # Group fixtures by year
        fixtures_by_year = {}
        for fixture in fixtures:
            year = fixture.match_date.year
            if year not in fixtures_by_year:
                fixtures_by_year[year] = []
            fixtures_by_year[year].append(fixture)

        for year, fixtures in fixtures_by_year.items():
            csv_filename = os.path.join(settings.MEDIA_ROOT, 'historical_fixtures', f'fixtures_{year}.csv')
            os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['home_team', 'away_team', 'match_date', 'round_number', 'match_stadium', 'home_logo', 'away_logo'])
                for fixture in fixtures:
                    writer.writerow([fixture.home_team, fixture.away_team, fixture.match_date, fixture.round_number, fixture.match_stadium, fixture.home_logo.url, fixture.away_logo.url])

            # Save the file reference in HistoricalFixtureFile model
            HistoricalFixtureFile.objects.create(year=year, file=f'historical_fixtures/fixtures_{year}.csv')

            self.stdout.write(self.style.SUCCESS(f'Successfully exported fixtures for {year} to {csv_filename}'))
