from django.contrib import admin
from .models import Movie

# TODO: Admin functionality not fully implemented
# Basic admin interface for development purposes only
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'updated']
    list_filter = ['genre', 'updated']
    search_fields = ['name', 'genre']
