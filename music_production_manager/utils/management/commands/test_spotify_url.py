from django.core.management.base import BaseCommand
from utils.spotify_utils import get_track_info

class Command(BaseCommand):
    help = 'Test the get_track_info function with a Spotify URL'

    def add_arguments(self, parser):
        parser.add_argument('spotify_url', type=str, help='Spotify track URL to test')

    def handle(self, *args, **options):
        spotify_url = options['spotify_url']
        self.stdout.write(self.style.SUCCESS(f'Testing URL: {spotify_url}'))
        
        try:
            result = get_track_info(spotify_url)
            if isinstance(result, dict):
                for key, value in result.items():
                    self.stdout.write(self.style.SUCCESS(f'{key}: {value}'))
            else:
                self.stdout.write(self.style.ERROR(f'Error: {result}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))