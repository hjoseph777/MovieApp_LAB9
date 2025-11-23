from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Populate the database with sample movie data'

    def handle(self, *args, **options):
        # Clear existing movies
        Movie.objects.all().delete()
        
        # Create sample movies
        movies_data = [
            {
                'name': 'The Shawshank Redemption',
                'genre': 'Drama',
                'description': 'A man wrongfully imprisoned finds hope and redemption through the common decency of the men serving time with him.'
            },
            {
                'name': 'The Godfather',
                'genre': 'Crime',
                'description': 'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.'
            },
            {
                'name': 'Inception',
                'genre': 'Sci-Fi',
                'description': 'A thief who steals secrets from dreams is given the final job of planting an idea deep within a target\'s subconscious.'
            },
            {
                'name': 'The Dark Knight',
                'genre': 'Action',
                'description': 'Batman faces his greatest challenge yet as the Joker wreaks havoc and chaos on Gotham City.'
            },
            {
                'name': 'Forrest Gump',
                'genre': 'Drama',
                'description': 'A man with a low IQ accomplishes great things in his life and influences the lives of those around him.'
            }
        ]
        
        for movie_data in movies_data:
            Movie.objects.create(**movie_data)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created movie: {movie_data["name"]}')
            )
        
        total = Movie.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'🎬 Successfully populated database with {total} movies!')
        )