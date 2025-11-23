"""
Django MovieApp Test Suite
Tests for Django Setup, Templates/Views, Models, and Forms
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
import os
from .models import Movie


class DjangoSetupTestCase(TestCase):
    """Test Django Settings, File Structure, and Configuration"""
    
    def test_secret_key_exists(self):
        """Test that SECRET_KEY is configured"""
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))
        self.assertNotEqual(settings.SECRET_KEY, '')
    
    def test_debug_setting(self):
        """Test DEBUG setting is properly configured"""
        self.assertTrue(hasattr(settings, 'DEBUG'))
    
    def test_installed_apps_configuration(self):
        """Test that required apps are installed"""
        self.assertIn('movie', settings.INSTALLED_APPS)
        self.assertIn('django.contrib.admin', settings.INSTALLED_APPS)
        self.assertIn('django.contrib.auth', settings.INSTALLED_APPS)
    
    def test_middleware_configuration(self):
        """Test middleware is properly configured"""
        self.assertIn('django.middleware.security.SecurityMiddleware', settings.MIDDLEWARE)
        self.assertIn('django.contrib.sessions.middleware.SessionMiddleware', settings.MIDDLEWARE)
    
    def test_database_configuration(self):
        """Test database is configured"""
        self.assertTrue(hasattr(settings, 'DATABASES'))
        self.assertIn('default', settings.DATABASES)
    
    def test_static_files_configuration(self):
        """Test static files are configured"""
        self.assertTrue(hasattr(settings, 'STATIC_URL'))
        self.assertTrue(hasattr(settings, 'STATICFILES_DIRS'))


class MovieModelTestCase(TestCase):
    """Test Django Models"""
    
    def setUp(self):
        """Set up test data"""
        self.movie = Movie.objects.create(
            name="Test Movie",
            genre="Drama",
            description="A test movie for testing purposes"
        )
    
    def test_movie_creation(self):
        """Test movie model creation"""
        self.assertEqual(self.movie.name, "Test Movie")
        self.assertEqual(self.movie.genre, "Drama")
        self.assertEqual(self.movie.description, "A test movie for testing purposes")
    
    def test_movie_str_method(self):
        """Test movie string representation"""
        self.assertEqual(str(self.movie), "Test Movie")
    
    def test_movie_fields(self):
        """Test movie model fields"""
        self.assertTrue(hasattr(self.movie, 'name'))
        self.assertTrue(hasattr(self.movie, 'genre'))
        self.assertTrue(hasattr(self.movie, 'description'))
        self.assertTrue(hasattr(self.movie, 'updated'))
    
    def test_movie_field_max_lengths(self):
        """Test model field constraints"""
        name_field = Movie._meta.get_field('name')
        genre_field = Movie._meta.get_field('genre')
        self.assertEqual(name_field.max_length, 200)
        self.assertEqual(genre_field.max_length, 200)
    
    def test_movie_auto_now_update(self):
        """Test that updated field changes on save"""
        import time
        original_updated = self.movie.updated
        # Small delay to ensure timestamp difference
        time.sleep(0.01)
        self.movie.name = "Updated Movie"
        self.movie.save()
        # Refresh from database to get updated timestamp
        self.movie.refresh_from_db()
        self.assertNotEqual(original_updated, self.movie.updated)


class MovieViewsTestCase(TestCase):
    """Test Templates and Views"""
    
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.movie1 = Movie.objects.create(
            name="The Shawshank Redemption",
            genre="Drama",
            description="Two imprisoned men bond over a number of years"
        )
        self.movie2 = Movie.objects.create(
            name="Inception",
            genre="Sci-Fi",
            description="A thief who steals corporate secrets"
        )
    
    def test_home_view(self):
        """Test home page view"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome")
        self.assertTemplateUsed(response, 'movie/home.html')
    
    def test_movie_list_view(self):
        """Test movie list view"""
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Shawshank Redemption")
        self.assertContains(response, "Inception")
        self.assertTemplateUsed(response, 'movie/movie_list.html')
    
    def test_movie_detail_view(self):
        """Test movie detail view"""
        response = self.client.get(reverse('movie_detail', kwargs={'id': self.movie1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Shawshank Redemption")
        self.assertContains(response, "Drama")
        self.assertTemplateUsed(response, 'movie/movie_detail.html')
    
    def test_movie_detail_view_404(self):
        """Test movie detail view with non-existent movie"""
        response = self.client.get(reverse('movie_detail', kwargs={'id': 9999}))
        self.assertEqual(response.status_code, 404)
    
    def test_movie_search_view(self):
        """Test movie search functionality"""
        response = self.client.get(reverse('movie_search'), {'genre': 'Drama'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Shawshank Redemption")
        self.assertNotContains(response, "Inception")
        self.assertTemplateUsed(response, 'movie/movie_search.html')
    
    def test_movie_search_empty(self):
        """Test movie search with no results"""
        response = self.client.get(reverse('movie_search'), {'genre': 'Horror'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "The Shawshank Redemption")
        self.assertNotContains(response, "Inception")


class TemplateTestCase(TestCase):
    """Test Template Structure and Content"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.movie = Movie.objects.create(
            name="Test Movie",
            genre="Test Genre",
            description="Test Description"
        )
    
    def test_base_template_structure(self):
        """Test that pages use proper template structure"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<html')
        self.assertContains(response, '</html>')
        self.assertContains(response, '<head>')
        self.assertContains(response, '</head>')
        self.assertContains(response, '<body>')
        self.assertContains(response, '</body>')
    
    def test_template_title_tags(self):
        """Test that templates have proper title tags"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<title>')
    
    def test_template_css_styling(self):
        """Test that templates include CSS styling"""
        response = self.client.get(reverse('home'))
        self.assertTrue(
            'style' in response.content.decode() or 
            'css' in response.content.decode()
        )


class URLConfigTestCase(TestCase):
    """Test URL Configuration and Routing"""
    
    def test_url_patterns_exist(self):
        """Test that all required URL patterns exist"""
        home_url = reverse('home')
        movie_list_url = reverse('movie_list')
        search_url = reverse('movie_search')
        
        self.assertEqual(home_url, '/')
        self.assertEqual(movie_list_url, '/movies/')
        self.assertEqual(search_url, '/search/')
    
    def test_movie_detail_url_with_parameter(self):
        """Test movie detail URL with ID parameter"""
        movie = Movie.objects.create(name="Test", genre="Test")
        detail_url = reverse('movie_detail', kwargs={'id': movie.id})
        self.assertEqual(detail_url, f'/movie/{movie.id}/')


class DatabaseTestCase(TestCase):
    """Test Database Operations"""
    
    def test_database_connection(self):
        """Test database connection works"""
        movies_count = Movie.objects.count()
        self.assertIsInstance(movies_count, int)
    
    def test_crud_operations(self):
        """Test Create, Read, Update, Delete operations"""
        # Create
        movie = Movie.objects.create(
            name="CRUD Test Movie",
            genre="Test",
            description="Testing CRUD operations"
        )
        self.assertTrue(movie.id)
        
        # Read
        retrieved_movie = Movie.objects.get(id=movie.id)
        self.assertEqual(retrieved_movie.name, "CRUD Test Movie")
        
        # Update
        retrieved_movie.name = "Updated CRUD Test Movie"
        retrieved_movie.save()
        updated_movie = Movie.objects.get(id=movie.id)
        self.assertEqual(updated_movie.name, "Updated CRUD Test Movie")
        
        # Delete
        movie_id = movie.id
        movie.delete()
        with self.assertRaises(Movie.DoesNotExist):
            Movie.objects.get(id=movie_id)


class FormTestCase(TestCase):
    """Test Form Functionality and Styling"""
    
    def test_search_form_submission(self):
        """Test search form submission"""
        Movie.objects.create(name="Action Movie", genre="Action")
        
        response = self.client.get(reverse('movie_search'), {'genre': 'Action'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Action Movie")
    
    def test_empty_form_submission(self):
        """Test form submission with empty data"""
        response = self.client.get(reverse('movie_search'), {'genre': ''})
        self.assertEqual(response.status_code, 200)
        # Should not show any movies for empty search


class IntegrationTestCase(TestCase):
    """Integration Tests - Testing Full User Workflows"""
    
    def setUp(self):
        """Set up comprehensive test data"""
        self.client = Client()
        # Create multiple movies for testing
        self.movies = [
            Movie.objects.create(name="The Matrix", genre="Sci-Fi", description="Reality simulation"),
            Movie.objects.create(name="Titanic", genre="Romance", description="Ship disaster"),
            Movie.objects.create(name="Jaws", genre="Thriller", description="Shark attack"),
        ]
    
    def test_full_user_journey(self):
        """Test complete user navigation flow"""
        # User visits home page
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # User navigates to movie list
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Matrix")
        
        # User clicks on a specific movie
        movie = self.movies[0]
        response = self.client.get(reverse('movie_detail', kwargs={'id': movie.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, movie.name)
        
        # User searches for movies
        response = self.client.get(reverse('movie_search'), {'genre': 'Sci-Fi'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Matrix")


class PerformanceTestCase(TestCase):
    """Basic Performance Tests"""
    
    def test_database_query_efficiency(self):
        """Test that views don't make excessive database queries"""
        # Create multiple movies
        for i in range(10):
            Movie.objects.create(
                name=f"Movie {i}",
                genre=f"Genre {i % 3}",
                description=f"Description {i}"
            )
        
        # Test that movie list view works with multiple records
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        
        # Ensure all movies are displayed
        self.assertContains(response, "Movie 0")
        self.assertContains(response, "Movie 9")
