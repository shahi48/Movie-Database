from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from .models import Movie, Review
from .forms import ReviewForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm

def movie_list(request):
    # Get all movies initially
    movies_list = Movie.objects.all().order_by('-release_date')
    
    # Get search query
    search_query = request.GET.get('search', '')
    if search_query:
        movies_list = movies_list.filter(
            Q(title__icontains=search_query) |
            Q(director__icontains=search_query) |
            Q(cast__icontains=search_query) |
            Q(genre__icontains=search_query) |
            Q(language__icontains=search_query)
        )

    # Get filter values
    genre_filter = request.GET.get('genre', '')
    language_filter = request.GET.get('language', '')

    # Apply filters
    if genre_filter:
        movies_list = movies_list.filter(genre=genre_filter)
    if language_filter:
        movies_list = movies_list.filter(language=language_filter)

    # Pagination
    paginator = Paginator(movies_list, 9)  # Show 9 movies per page
    page = request.GET.get('page')
    movies = paginator.get_page(page)

    # Get unique genres and languages for filter dropdowns
    genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre')
    languages = Movie.objects.values_list('language', flat=True).distinct().order_by('language')

    context = {
        'movies': movies,
        'search_query': search_query,
        'genre_filter': genre_filter,
        'language_filter': language_filter,
        'genres': [(genre, genre) for genre in genres],
        'languages': [(lang, lang) for lang in languages],
        'total_movies': movies.paginator.count if movies else 0,
    }
    
    return render(request, 'movies/movie_list.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    has_reviewed = False
    if request.user.is_authenticated:
        has_reviewed = Review.objects.filter(movie=movie, user=request.user).exists()
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'has_reviewed': has_reviewed
    })

@login_required
def toggle_favorite(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if movie.favorites.filter(id=request.user.id).exists():
        movie.favorites.remove(request.user)
        messages.success(request, f'Removed {movie.title} from favorites')
    else:
        movie.favorites.add(request.user)
        messages.success(request, f'Added {movie.title} to favorites')
    return redirect('movie_detail', movie_id=movie_id)

@login_required
def favorite_movies(request):
    movies = request.user.favorite_movies.all()
    return render(request, 'movies/favorite_movies.html', {'movies': movies})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movie_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.method == 'POST':
        # Check if user has already reviewed this movie
        if Review.objects.filter(movie=movie, user=request.user).exists():
            messages.error(request, 'You have already reviewed this movie.')
            return redirect('movie_detail', movie_id=movie_id)
        
        # Create new review
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        
        if rating and text:
            Review.objects.create(
                movie=movie,
                user=request.user,
                rating=rating,
                text=text
            )
            messages.success(request, 'Your review has been added successfully!')
        else:
            messages.error(request, 'Please provide both rating and review text.')
            
    return redirect('movie_detail', movie_id=movie_id)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('movie_list')
