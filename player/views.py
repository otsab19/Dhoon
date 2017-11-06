from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from math import sqrt
from .forms import UserForm, SongForm, AlbumForm
from .models import Song, Album, Rating

# Create your views here.

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMG_TYPES = ['png', 'jpg', 'jpeg']

def index(request):
	if not request.user.is_authenticated():
		return render(request, 'login.html')
	else:
		cuser = request.user
		print(cuser)
		albums = Album.objects.filter(user=request.user)
		song_results = Song.objects.all()
		query = request.GET.get("q")
		if query:
			albums = albums.filter(
				Q(album_title__icontains=query) |
				Q(artist__icontains=query)
			).distinct()
			song_results = song_results.filter(
				Q(name__icontains=query)
			).distinct()
			print(song_results)
			data = []
			user_ratings = []
			print(data,user_ratings)
			for csong in song_results:
				print("song yo ho", csong)
				try:
					print("try ma gaayo")
					rate = Rating.objects.filter(song=csong, user=cuser)
					print("rate query successful vayo")
					for let in str(rate):
						if let.isdigit():
							num = let
							break;
					num = int(num)
					print(num)
					user_ratings.append(num)
					temp = (csong, num)
					print(temp)
				except:
					print("except ma gaayo")
					user_ratings.append(None)
					temp = (csong, None)
				finally:
					print("finally ma gaayo")
					data.append(temp)
			print("data agadi ko thau home ko")
			print(data)
			return render(request, 'home.html', {
				'albums':albums,
				'data':data,
				'user':request.user,
			})
		else:
			return render(request, 'home.html', {'albums': albums})

def create_album(request):
	if not request.user.is_authenticated():
		return render(request, 'login.html')
	else:
		form = AlbumForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			album = form.save(commit=False)
			album.user = request.user
			album.album_art = request.FILES['album_art']
			file_type = album.album_art.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in IMG_TYPES:
				context = {
					'album':album,
					'form':form,
					'error_message':'Image is not in required format.',
				}
				return render(request, 'create_album.html', context)
			album.save()
			return redirect('interface', album_id=album.pk)
		context = {
			'form':form,
		}
		return render(request, 'create_album.html', context)


def create_song(request, album_id):
	form = SongForm(request.POST or None, request.FILES or None)
	album = get_object_or_404(Album, pk=album_id)
	if form.is_valid():
		album_songs = album.song_set.all()
		for sng in album_songs:
			if sng.name == form.cleaned_data.get("name"):
				context = {
					'album':album,
					'form':form,
					'error_message': 'Song Already Added.',
				}
				return render(request, 'create_song.html', context)
		song = form.save(commit=False)
		song.album = album
		song.audio = request.FILES['audio']
		file_type = song.audio.url.split('.')[-1]
		file_type = file_type.lower()
		if file_type not in AUDIO_FILE_TYPES:
			context = {
				'album':album,
				'form':form,
				'error_message':'Audio file is not of required format.',				
				}
			return render(request, 'create_song.html', context)

		song.save()
		return redirect('interface', album_id=album.pk)
	context = {
		'album':album,
		'form':form,
		}
	return render(request, 'create_song.html', context)

def delete_album(request, album_id):
	album = Album.objects.get(pk=album_id)
	album.delete()
	#albums = Album.objects.filter(user=request.user)
	return redirect('index')

def delete_song(request, album_id, song_id):
	album = get_object_or_404(Album, pk=album_id)
	song = Song.objects.get(pk=song_id)
	song.delete()
	return redirect('interface', album_id=album.pk)


def logout_user(request):
	logout(request)
	form = UserForm(request.POST or None)
	context = {
		'form':form
	}
	#return render(request, 'login.html', context)
	return redirect('index')

def interface(request, album_id):
	if not request.user.is_authenticated():
		return render(request, 'login.html')
	else:
		user = request.user
		album = get_object_or_404(Album, pk=album_id)
		data = []
		user_ratings = []
		for song in album.song_set.all():
			try:
				rate = Rating.objects.get(song=song, user=user)
				#print(rate, rate.star)
				user_ratings.append(rate.star)
				temp = (song,rate.star)
			except:
				user_ratings.append(None)
				temp = (song,None)
			finally:
				data.append(temp)
		#print("data agadi ko thau interface ko")
		#print(data)
		# if request.method == "POST":
		# 	currentSongUrl = request.POST['currentSong']
		# 	currentSng = Song.objects.get(audio == currentSongUrl)
		# 	print(currentSng.listened)
		return render(request, 'interface.html', {'data':data, 'user':user, 'album':album})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				#albums = Album.objects.filter(user=request.user)
				#return render(request, 'home.html', {'albums':albums})
				return redirect('index')
			else:
				return render(request, 'login.html', {'error_message':'Account Deactivaated'})
		else:
			return render(request, 'login.html', {'error_message':'Invalid Login'})
	return render(request, 'login.html')

def register(request):
	form = UserForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username = username, password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				#if Album.objets.filter(user=request.user):
				album = Album.objects.filter(user=request.user)
			#	else:
			#		albums=None
				return render(request, 'home.html', {'album':album})
	context = {'form':form}
	return render(request, 'register.html', context)


def songs(request, filter_by):
	if not request.user.is_authenticated():
		return render(request, 'login.html')
	else:
		try:
			song_ids = []
			for album in Album.objects.filter(user=request.user):
				for song in album.song_set.all():
					song_ids.append(song.pk)
			users_songs = Song.objects.filter(pk__in=song_ids)	
		except Album.DoesNotExist:
			users_songs = []
		return render(request, 'songs.html', {
				'song_list':users_songs,
				'filter_by':filter_by,
			})


def test(request):
	if not request.user.is_authenticated():
		return render(request, 'login.html')
	else:
		user=request.user
		if request.method == "POST":

			if request.is_ajax():

				currentSongName = request.POST.get('cSong',False)
				currentSng = Song.objects.get(name = currentSongName)
				users_who_have_listened = currentSng.listened.all()

				if request.user in users_who_have_listened:
					print("Already In Database")
				else:
					currentSng.listened.add(user)

				ratings = Rating.objects.filter(song=currentSng
					).exclude(user=user)

				users_who_rate_the_current_song = []
				for rate in ratings:
					users_who_rate_the_current_song.append(rate.user)
				print(users_who_rate_the_current_song, "\n\n")
				all_possible_songs = []
				avg_user_ratings = []
				for users in users_who_rate_the_current_song:
					temprate = Rating.objects.filter(user=users)
					avg_rating = 0
					for songs in temprate:
						tempsong = songs.song
						no_of_ratings_for_tempsong = len(Rating.objects.filter(song=tempsong))
						if no_of_ratings_for_tempsong >= 3:
							if tempsong not in all_possible_songs:
								all_possible_songs.append(tempsong)
							avg_rating+=songs.star
						avg_user_ratings.append(avg_rating/len(temprate))
				#print(all_possible_songs)


				similarity_weights = []
				nextSng = {}
				previous_weight = -2.0000
				for songs in all_possible_songs:
					print("sons="+songs.name)
					numerator = 0
					denominator = 1
					da,db = 0,0
					for users,user_avg_rate in zip(users_who_rate_the_current_song,avg_user_ratings):
						print(users.username)
						try:
							rate = Rating.objects.get(song=songs,user=users)
							nextSng_rate_by_user = rate.star
							try:
								rate = Rating.objects.get(song=currentSng,user=users)
								currentSng_rate_by_user = rate.star
							except:
								currentSng_rate_by_user = user_avg_rate
							print(currentSng_rate_by_user)
							na,nb = currentSng_rate_by_user-user_avg_rate,nextSng_rate_by_user-user_avg_rate
							numerator += na*nb
							da += na**2
							db += nb**2
						except:
							print(users.username +' has not rated the song '+songs.name)
							continue
						print("da=",da,"db=",db)
					denominator = sqrt(da*db)
					print("denominator=",denominator)
					weight = round(numerator/denominator, 4)
					print("weight=",weight)
					similarity_weights.append((songs,weight))
					if songs != currentSng:
						if weight > previous_weight:
							previous_weight = weight
							print(round(previous_weight,4), round(weight,4))
							nextOne = songs
						print(nextOne.audio.url, songs.name)
						nextSng = {'nextSngUrl':nextOne.audio.url, 'nextSngName':nextOne.name, 'artist':nextOne.album.artist, 'nextSngRating':None}
				print(similarity_weights)	


			return JsonResponse(nextSng)
		return JsonResponse({"response" : "Not Post"})
	#return render(request, 'test.html')


def rate(request):
	if not request.user.is_authenticated():
		return render(request, 'login.html')
	else:
		user = request.user
		if request.method == "POST":
			if request.is_ajax():
				print("rate ma ajax ho re")
				currentSongName = request.POST.get('cSong',False)
				rated_value = request.POST.get('star',False)
				#print(rated_value)
				currentSng = Song.objects.get(name=currentSongName)
				users_who_have_rated = []
				ratings = Rating.objects.filter(song=currentSng, user=user)
				for rate in ratings:
					#print("all users", rate.user)
					users_who_have_rated.append(rate.user)
				#print(users_who_have_rated)
				if user in users_who_have_rated:
					print("rate gari sakya re")
				else:
					rate = Rating(song=currentSng, user=user, star=rated_value)
					rate.save()
					#print("uncomment")
			return JsonResponse({'song_name':currentSongName, 'user_name':user.username})
		return JsonResponse({'response':"khai rate save vayena"})
