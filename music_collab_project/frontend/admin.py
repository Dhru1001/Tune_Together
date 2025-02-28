from django.contrib import admin
from .models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'bio', 'profile_picture')  # Display role
    search_fields = ('user__username', 'role')  # Allow searching by username or role
    list_filter = ('role',)  # Filter by roles, e.g., musician, listener


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    search_fields = ('title', 'artist')
    list_filter = ('release_date',)
    ordering = ('release_date',)

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'profile_url')
    search_fields = ('name', 'genre')
    list_filter = ('genre',)
    ordering = ('name',)

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "release_date", "album", "duration", "genre", "created_at", "play_count")
    list_filter = ("artist", "album", "release_date")
    search_fields = ("title", "artist__name", "album__title", "genre__name")
    ordering = ('release_date',)

@admin.register(LikedSong)
class LikedTracksAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'liked_at')
    search_fields = ('user__username', 'track__title')
    list_filter = ('liked_at',)
    ordering = ('liked_at',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('preferences',)
    search_fields = ('user__username',)
    ordering = ('user',)

# Customizing the admin site header
admin.site.site_header = "Artist Management Admin"
admin.site.site_title = "Artist Admin Portal"
admin.site.index_title = "Welcome to the Artist Management Dashboard"
