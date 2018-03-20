from django.shortcuts import render, redirect
from .models import Profile, Post, FavoritePost, Follow
from django.contrib.auth.models import User
from .forms import UserForm, UpdateProfile, CreatePostForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


# Create your views here.

def user_logout(request):
	logout(request)
	return redirect("login")



def user_login(request):
	form = LoginForm()
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			my_username = form.cleaned_data['username']
			my_password = form.cleaned_data['password']
			auth_user = authenticate(username=my_username, password=my_password)
			if auth_user is not None:
				login(request,auth_user)
				return redirect("home")
	context = {
		"form": form
	}
	return render(request, 'login.html', context)



def home(request):
	posts = Post.objects.all()
	user = request.user
	profile = Profile.objects.filter(user=user)
	fav_posts = Post.objects.filter(user=profile)
	fav_posts = []
	favs = request.user.favoritepost_set.all()
	for fav in favs:
		fav_posts.append(fav.post)
	context={
		'posts' : posts,
		'fav_posts': fav_posts,
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

def signup(request):
	form = UserForm()
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save()
			profile = Profile.objects.create(user=user)
			profile.save()
			return redirect('home')
	context = {
		"form":form
	}
	return render(request, 'signup.html', context)

def update_profile(request,profile_id):
	profile = Profile.objects.get(id=profile_id)
	form = UpdateProfile(instance=profile)
	if request.method == "POST":
		form = UpdateProfile(request.POST, request.FILES or None, instance=profile)
		if form.is_valid():
			form.save()
			return redirect('profile' ,profile_id=profile.id)
	context = {
		'profile':profile,
		'form':form,
	}
	return render(request, 'update_profile.html', context)

def create_post(request):
	if(request.user.is_anonymous):
			return redirect('login')
	form = CreatePostForm()
	if request.method == "POST":
		form = CreatePostForm(request.POST, request.FILES or None)
		if form.is_valid():
			form.save()
			return redirect("home")
	context = {
	"create_form": form,
	}
	return render(request, 'create_post.html', context)


def favorite_post(request, post_id):
	post_obj = Post.objects.get(id=post_id)
	favorite_obj, created = FavoritePost.objects.get_or_create(user=request.user, post=post_obj)
	if created:
		action = 'fav'
	else:
		action = 'notfav'
		favorite_obj.delete()
	fav_num = post_obj.favoritepost_set.all().count()
	response = {
		"action": action,
		"fav_num": fav_num,
	}
	return JsonResponse(response, safe=False)
