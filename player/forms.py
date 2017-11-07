from django.contrib.auth.models import User
from django import forms
from .models import Song, Album

class UserForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ['username','email','password']

class SongForm(forms.ModelForm):

	class Meta:
		model = Song
		fields = ['name', 'audio']

class AlbumForm(forms.ModelForm):

	class Meta:
		model = Album
		fields = ['artist', 'album_title', 'genre','album_art']