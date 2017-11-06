from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.
class Album(models.Model):
	user = models.ForeignKey(User, default=1)
	album_title = models.CharField(max_length=50)
	artist = models.CharField(max_length=50)
	genre = models.CharField(max_length=50)
	album_art = models.FileField()


	def __str__(self):
		return self.album_title+"-"+self.artist


class Song(models.Model):
	album = models.ForeignKey(Album, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)#None=False, Blank=False)
	audio = models.FileField()
	#rating = models.ManyToManyField(User, related_name='rating_set', default=1)
	listened = models.ManyToManyField(User, related_name='listened_set', default=1)

	def __str__(self):
		return self.name

class Rating(models.Model):
	song = models.ForeignKey(Song, related_name='song_star', default=1)
	user = models.ForeignKey(User, related_name='song_user', default=1)
	star = models.IntegerField()

	def __str__(self):
		return str(self.star)



