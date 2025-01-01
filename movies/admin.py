from django.contrib import admin
from .models import Movie, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'genre', 'language', 'release_date')
    list_filter = ('genre', 'language')
    search_fields = ('title', 'director', 'cast')
    date_hierarchy = 'release_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('movie__title', 'user__username', 'text')
