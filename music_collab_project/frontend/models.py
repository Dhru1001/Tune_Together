from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='album_covers/')
    release_date = models.DateField(null=True, blank=True)
    slug = models.SlugField(unique=True) 
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate a slug from the album title
            # Ensure slug is unique by checking if it already exists
            original_slug = self.slug
            queryset = Album.objects.filter(slug=self.slug)
            if queryset.exists():
                count = queryset.count()
                self.slug = f"{original_slug}-{count + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Artist(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='artists/')
    genre = models.CharField(max_length=50, default='Unknown')
    profile_url = models.URLField(default='#')  # Link to artist's page or genre

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    background_image = models.ImageField(upload_to='genre_backgrounds/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # New description field
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Generate a slug from the album title
            # Ensure slug is unique by checking if it already exists
            original_slug = self.slug
            queryset = Genre.objects.filter(slug=self.slug)
            if queryset.exists():
                count = queryset.count()
                self.slug = f"{original_slug}-{count + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Track(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    release_date = models.DateField()
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)  # Updated to ForeignKey
    duration = models.DurationField()
    cover_image = models.ImageField(upload_to="track_covers/", blank=True, null=True)
    audio_file = models.FileField(upload_to="audio_files/", blank=True, null=True)  # New field for audio files
    genre = models.ForeignKey(Genre, related_name='tracks', on_delete=models.CASCADE)  # New field to associate tracks with genres
    play_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title} by {self.artist}"


class LikedSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_songs')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} likes {self.track.title}"

class Playlist(models.Model):
    user = models.ForeignKey(User, related_name='playlists', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    tracks = models.ManyToManyField(Track, related_name='playlists')  # Many-to-many relationship with Track
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user.username}"

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('listener', 'Listener'),
        ('musician', 'Musician'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='listener')  # Add role field

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


    
    

class Preference(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preferences = models.ManyToManyField(Preference)

    def __str__(self):
        return f"{self.user.username}'s Preferences"



class CollaborationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=100)  # e.g., "Producer Needed"
    status = models.CharField(max_length=20, default='pending')  # e.g., "pending", "accepted", "declined"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
