from django.urls import path
from frontend.views import *

urlpatterns = [
    path("", home, name="home"),
    path("trial", trail, name="trail"),
    path("main", main, name="main"),
    path("discover", discover, name="discover"),
    path('view-all-albums/', view_all_albums, name='view_all_albums'),
    path('view-all-artists/', view_all_artists, name='view_all_artists'),
    path('view-all-genres/', view_all_genres, name='view_all_genres'),
    path('login/', custom_login, name='login'),  # Custom login
    path('logout/', custom_logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('liked_songs/', liked_songs, name='liked_songs'),
    path('search/', search_view, name='search_view'),
    path('music-genres/', music_genres_view, name='music_genres'),
    path('most-played/', most_played, name='most_played'),
    path('recently-added/', recently_added, name='recently_added'),
    path('your_playlists/', your_playlists, name='your_playlists'),
    path('add_playlist/', add_playlist, name='add_playlist'),
    path('musician_dashboard/', musician_dashboard, name='musician_dashboard'),
    path('preferences/', preference_selection, name='preference_selection'),
    path('create-collaboration/', create_collaboration_request, name='create_collaboration_request'),
    path('collaboration/accept/<int:request_id>/', accept_collaboration, name='accept_collaboration'),
    path('collaboration/decline/<int:request_id>/', decline_collaboration, name='decline_collaboration'),
    path('collaboration/<int:project_id>/', collaboration_dashboard, name='collaboration_dashboard'),
    path('collaboration/<int:project_id>/send-message/', send_collaboration_message, name='send_collaboration_message'),
    path('send-message/<int:project_id>/', send_collaboration_message, name='send_message'),
    path('update-task/<int:task_id>/', update_task, name='update_task'),
    path('add-task/<int:project_id>/', add_task, name='add_task'),
    path('upload/', upload_track, name='upload_track'),
    path('add-artist/', add_artist, name='add_artist'),
    path('add-album/', add_album, name='add_album'),
    path('add_genre/', add_genre, name='add_genre'),

    path('increment-play-count/<int:track_id>/', increment_play_count, name='increment_play_count'),
    path('album/<slug:album_slug>/', album_songs_view, name='album_songs'),
    path('genre/<slug:slug>/', genre_detail_view, name='genre_detail'),

    path('<str:artist_name>/', artist_tracks, name='artist_tracks'),
    path('playlist/<int:playlist_id>/', playlist_detail, name='playlist_detail'),
    path('like-song/<int:track_id>/', like_song, name='like_song'),

]
