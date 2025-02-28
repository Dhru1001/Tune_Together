from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Import the login decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .forms import  TrackUploadForm
from .models import *


def signup(request):
    """
    Handles user signup.

    Parameters:
    request (HttpRequest): The incoming request object. This object contains information about the HTTP request, including the method (GET, POST), headers, and data.

    Returns:
    HttpResponse: The rendered signup template or a redirect to the login page upon successful signup.
    If the request method is POST, the function validates the user creation form and saves the new user if the form is valid.
    If the request method is GET, the function renders the signup template with an empty user creation form.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Ensure profile exists
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
                
            user.profile.role = request.POST.get('role', 'listener')
            user.profile.save()
            
            messages.success(request, "Account created! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def custom_login(request):
    """
    Handles user login.

    Parameters:
    request (HttpRequest): The incoming request object. This object contains information about the HTTP request, including the method (GET, POST), headers, and data.

    Returns:
    HttpResponse: The rendered login template, a redirect to the main page upon successful login, or a redirect to the next URL if provided.
    If the request method is POST, the function validates the authentication form and logs in the user if the form is valid.
    If the request method is GET, the function renders the login template with an empty authentication form.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                if user.profile.role == 'musician':
                    return redirect('musician_dashboard')
                else:
                    return redirect('main')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def custom_logout(request):
    logout(request)
    return redirect('main')

# Home page (public)
def home(request):
    return render(request, "home.html")

# Trial page (public)
def trail(request):
    return render(request, "trial.html")

# Main page (public)
def main(request):
    albums = Album.objects.all()  # Retrieve all albums
    artists = Artist.objects.all()  # Retrieve all artists
    genres = Genre.objects.all() 
    return render(request, "main.html", {'albums': albums, 'artists': artists, 'genres': genres})

# Discover page (public)
def discover(request):
    artists = Artist.objects.all()
    return render(request, "discover.html", {'artists': artists})

def most_played(request):
    # Assuming you have a 'play_count' field that tracks the number of plays
    tracks = Track.objects.all().order_by('-play_count')[:10] # Top 10 most played tracks
    return render(request, 'most_played.html', {'tracks': tracks, 'is_authenticated': request.user.is_authenticated})

def recently_added(request):
    # Fetch tracks ordered by their creation date (assuming a `created_at` field exists in your Track model)
    # Limit to the 10 most recent tracks
    tracks = Track.objects.all().order_by('-created_at')[:10]
    return render(request, 'recently_added.html', {'tracks': tracks})  

def increment_play_count(request, track_id):
    if request.method == 'POST':
        try:
            track = Track.objects.get(id=track_id)
            track.play_count += 1
            track.save()
            return JsonResponse({'success': True})
        except Track.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Track not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def view_all_albums(request):
    albums = Album.objects.all()
    return render(request, "view_all_albums.html", {'albums': albums})


def view_all_artists(request):
    artists = Artist.objects.all()
    return render(request, "discover.html", {'artists': artists})

def artist_list(request):
    # Get all artists from the database
    artists = Artist.objects.all()
    
    # Pass the artists to the template
    return render(request, 'discover.html', {'artists': artists})


def album_songs_view(request, album_slug):
    album = get_object_or_404(Album, slug=album_slug)  # Make sure the slug is passed correctly
    context = {
        'album': album,
        'songs': album.songs.all(),
        'is_authenticated': request.user.is_authenticated,# Use 'songs' instead of 'track_set'
    }
    return render(request, 'album_details.html', context)

def view_all_genres(request):
    # Get all genres from the database
    genres = Genre.objects.all()

    # Render the template with the genres data
    return render(request, 'view_all_genres.html', {
        'genres': genres,
    })

def music_genres_view(request):
    genres = Genre.objects.all()  # Fetch all genres
    return render(request, 'music_geners.html', {'genres': genres})

def genre_detail_view(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    track = Track.objects.all()
    return render(request, 'genre_detail.html', {'genre': genre, 'track': track, 'is_authenticated': request.user.is_authenticated})


def artist_tracks(request, artist_name):
    """
    Retrieves and displays tracks for a specific artist, along with liked tracks for authenticated users.

    This function filters tracks based on the given artist name, determines which tracks are liked
    by the authenticated user (if any), and renders a template with this information.

    Parameters:
    request (HttpRequest): The HTTP request object containing metadata about the request,
                           including user authentication status.
    artist_name (str): The name of the artist whose tracks are to be displayed. Hyphens in the
                       name are replaced with spaces for URL-friendly handling.

    Returns:
    HttpResponse: A rendered HTML response containing the artist's tracks, liked tracks (for
                  authenticated users), and authentication status. The response is based on
                  the 'artist_tracks.html' template.
    """
    # Filter tracks for the given artist (replace hyphens with spaces for URL-friendly names)
    tracks = Track.objects.filter(artist__icontains=artist_name.replace("-", " "))

    # Initialize liked_tracks_ids as empty
    liked_tracks_ids = []

    # Check if the user is authenticated before querying liked songs
    if request.user.is_authenticated:
        liked_songs = LikedSong.objects.filter(user=request.user)
        liked_tracks_ids = liked_songs.values_list('track_id', flat=True)  # List of liked track IDs

    return render(request, 'artist_tracks.html', {
        'artist_name': artist_name,  # Pass the artist name for display in the template
        'tracks': tracks,  # Pass the list of tracks to the template
        'liked_tracks_ids': liked_tracks_ids,  # Pass the liked tracks IDs for button state
        'is_authenticated': request.user.is_authenticated,  # Pass whether the user is authenticated
    })




@login_required
def your_playlists(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'your_playlists.html', {'playlists': playlists})

def playlist_detail(request, playlist_id):
    """
    Retrieves and displays the details of a specific playlist for the authenticated user.

    Parameters:
    request (HttpRequest): The HTTP request object containing metadata about the request.
    playlist_id (int): The unique identifier of the playlist to be retrieved.

    Returns:
    HttpResponse: A rendered HTML response containing the playlist details and its associated tracks.
                If the playlist is not found or doesn't belong to the user, it raises a 404 error.
    """
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    tracks = playlist.tracks.all()  # Assuming 'tracks' is a related field in your Playlist model
    return render(request, 'playlist_detail.html', {'playlist': playlist, 'tracks': tracks})

@login_required
def add_playlist(request):
    """
    Handles the addition of a new playlist by a logged-in user.

    Parameters:
    request (HttpRequest): The incoming request object. This object contains information about the HTTP request, including the method (GET, POST), headers, and data.

    Returns:
    HttpResponse: If the request method is POST, the function creates a new playlist with the provided name, description, and selected tracks, saves it, and redirects to the user's playlists page.
                 If the request method is GET, the function renders the 'add_playlist.html' template with a list of all tracks.

    Note:
    This function assumes that the user is authenticated and that the necessary models (Playlist, Track) are defined in the project.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        track_ids = request.POST.getlist('tracks')  # Get selected tracks

        playlist = Playlist.objects.create(user=request.user, name=name, description=description)
        playlist.tracks.set(Track.objects.filter(id__in=track_ids))  # Add selected tracks to the playlist
        playlist.save()
        return redirect('your_playlists')  # Redirect to the playlists page

    tracks = Track.objects.all()
    return render(request, 'add_playlist.html', {'tracks': tracks})



# ... (other functions with similar documentation comments)
def like_song(request, track_id):
    """
    Handles liking or unliking a song.

    Parameters:
    request (HttpRequest): The incoming request object.
    track_id (int): The ID of the track to like or unlike.

    Returns:
    JsonResponse: A JSON response indicating whether the song was liked or unliked.
    """
    track = get_object_or_404(Track, id=track_id)  # Improved with get_object_or_404

    # Toggle functionality: create or delete a like
    liked_song, created = LikedSong.objects.get_or_create(user=request.user, track=track)

    if not created:
        liked_song.delete()  # Remove like if already liked
        return JsonResponse({'status': 'unliked'})

    return JsonResponse({'status': 'liked'})




def liked_songs(request):
    try:
        liked_songs = LikedSong.objects.filter(user=request.user).select_related('track')
    except Exception as e:
        print("Error Fetching Liked Songs:", e)
    return render(request, 'liked_songs.html', {'liked_songs': liked_songs, 'is_authenticated': request.user.is_authenticated})

def search_view(request):
    query = request.GET.get('query', '')  # Get the search query from the URL

    if query:
        # Search for tracks and artists that match the query
        tracks = Track.objects.filter(title__icontains=query)  # Search by track title
        artists = Artist.objects.filter(name__icontains=query)  # Search by artist name
    else:
        tracks = []
        artists = []

    return render(
        request,
        'search_results.html',  # The template to display search results
        {'query': query, 'tracks': tracks, 'artists': artists, 'is_authenticated': request.user.is_authenticated}
    )
    

def preference_selection(request):
    if request.method == 'POST':
        selected_preferences = request.POST.getlist('preferences')
        user_preference, created = UserPreference.objects.get_or_create(user=request.user)
        user_preference.preferences.set(Preference.objects.filter(id__in=selected_preferences))
        return redirect('home')  # Replace 'home' with the URL name of your homepage.

    preferences = Preference.objects.all()
    return render(request, 'preference_selection.html', {'preferences': preferences})





















@login_required
def musician_dashboard(request):
    # First check musician role
    if request.user.profile.role != 'musician':
        return redirect('main')
    
    try:
        # Get tracks for logged-in user
        user_tracks = Track.objects.filter(user=request.user)
        # Calculate metrics
        total_listens = sum(track.play_count for track in user_tracks)
        # followers_count = request.user.profile.followers.count()  # Fixed
        recent_uploads = user_tracks.order_by('-created_at')[:5]
        
        # Collaboration requests
        collaboration_requests = CollaborationRequest.objects.filter(
            status='pending', 
            user=request.user
        )
        
        context = {
            'total_listens': total_listens,
            # 'followers_count': followers_count,
            'revenue': calculate_revenue(request.user.profile),  # Pass profile
            'recent_uploads': recent_uploads,
            'collaboration_requests': collaboration_requests,
        }
        print(f"Context: {context}")  # Debug context
        print("=== DEBUG END ===\n")
        
        return render(request, 'musician_dashboard.html', context)
        
    except Exception as e:
        print(f"Error in dashboard: {str(e)}")
        return redirect('musician_dashboard')

def calculate_revenue(user_profile):
    # Implement your revenue calculation logic here
    return 1240 

@login_required
def create_collaboration_request(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        collaboration_type = request.POST.get('type')
        CollaborationRequest.objects.create(
            user=request.user,
            title=title,
            description=description,
            type=collaboration_type
        )
        messages.success(request, "Collaboration request created!")
        return redirect('musician_dashboard')
    return render(request, 'create_collaboration_request.html')

@login_required
def upload_track(request):
    if request.method == 'POST':
        form = TrackUploadForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.user = request.user
            track = form.save()  # Save the track
            messages.success(request, "Upload successful!")
            return redirect('musician_dashboard')
        else:
            messages.error(request, "Upload failed. Please correct the errors.")
    else:
        form = TrackUploadForm()
    
    artists = Artist.objects.all()
    genres = Genre.objects.all()
    albums = Album.objects.all()  # Fetch all albums

    return render(request, 'upload_track.html', {
        'form': form,
        'artists': artists,
        'genres': genres,
        'albums': albums  # Pass 'albums' to the template
    })

@login_required
def add_artist(request):
    if request.method == 'POST':
        artist_name = request.POST.get('new_artist_name')
        artist_image = request.FILES.get('new_artist_image')
        artist_genre = request.POST.get('new_artist_genre', 'Unknown')
        artist_profile_url = request.POST.get('new_artist_profile_url', '#')

        if artist_name and artist_image:
            Artist.objects.create(
                name=artist_name,
                image=artist_image,
                genre=artist_genre,
                profile_url=artist_profile_url
            )
            messages.success(request, "Artist added successfully!")
        else:
            messages.error(request, "Failed to add artist. Please provide a name and image.")
        return redirect('upload_track')
    return render(request, 'add_artist.html')

@login_required
def add_album(request):
    if request.method == 'POST':
        album_title = request.POST.get('new_album_title')
        album_artist = request.POST.get('new_album_artist')
        album_cover_image = request.FILES.get('new_album_cover_image')
        album_release_date = request.POST.get('new_album_release_date')

        if album_title and album_artist and album_cover_image:
            Album.objects.create(
                title=album_title,
                artist=album_artist,
                cover_image=album_cover_image,
                release_date=album_release_date
 )
            messages.success(request, "Album added successfully!")
        else:
            messages.error(request, "Failed to add album. Please provide all required fields.")
        return redirect('upload_track')
    return render(request, 'add_album.html')

@login_required
def add_genre(request):
    if request.method == 'POST':
        genre_name = request.POST.get('new_genre_name')
        description = request.POST.get('new_genre_description')
        background_image = request.FILES.get('new_genre_background_image')

        if genre_name:
            # Slug will be auto-generated in the model's save()
            Genre.objects.create(
                name=genre_name,
                description=description,
                background_image=background_image
            )
            messages.success(request, "Genre added successfully!")
        else:
            messages.error(request, "Failed to add genre. Please provide a name.")
        return redirect('upload_track')
    return render(request, 'add_genre.html')