from django.core.management.base import BaseCommand
from regional_app.fetcher import fetch_and_store_weather_data

class Command(BaseCommand):
    help = 'Fetch and store weather data from the UK Met Office'

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching weather data...")
        fetch_and_store_weather_data()
        self.stdout.write("Weather data fetched and stored successfully.")
