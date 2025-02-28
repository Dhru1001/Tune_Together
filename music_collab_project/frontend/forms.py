from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Track, Artist, Album, Genre

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('listener', 'Listener'),
        ('musician', 'Musician'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'input-field'}))
    
    


class TrackUploadForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artist', 'album', 'genre', 'release_date', 'duration', 'cover_image', 'audio_file']
    
    artist = forms.ModelChoiceField(queryset=Artist.objects.all())
    album = forms.ModelChoiceField(queryset=Album.objects.all())
    genre = forms.ModelChoiceField(queryset=Genre.objects.all())