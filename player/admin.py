from django.contrib import admin

# Register your models here.
from .models import Song, Album, Rating

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Rating)