from django.shortcuts import render, get_object_or_404
from .models import Movie

def home(request):
    """Welcome homepage - no movies shown initially"""
    return render(request, 'movie/home.html')

def movie_list(request):
    """Display all movies when explicitly requested"""
    movies = Movie.objects.all()
    return render(request, 'movie/movie_list.html', {'movies': movies})

def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, 'movie/movie_detail.html', {'movie': movie})

def movie_search(request):
    genre = request.GET.get('genre', '')
    movies = Movie.objects.filter(genre__icontains=genre) if genre else []
    return render(request, 'movie/movie_search.html', {'movies': movies, 'genre': genre})