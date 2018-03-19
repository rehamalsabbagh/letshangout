from django.shortcuts import render, redirect
from .models import Profile, Post, Favorite, Follow
from django.contrib.auth.models import User


# Create your views here.

def home(request):
	posts = Post.objects.all()
	context={
		'posts' : posts,
	}
	return render(request, 'home.html', context)

def profile(request,profile_id):
	profile = Profile.objects.get(id=profile_id)
	posts = Post.objects.filter(user=profile)
	context={
		'profile': profile,
		'posts' : posts,
	}
	return render(request, 'profile.html', context)
