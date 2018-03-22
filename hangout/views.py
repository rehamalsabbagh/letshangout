from django.shortcuts import render, redirect
from .models import Profile, Post, FavoritePost, Follow, Followers
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
	me =  Profile.objects.get(user=request.user)
	# following = Follow.objects.filter(me=me)
	# following = Profile.followers_set.filter(user=me)
	# print(following)
	user = request.user
	profile = Profile.objects.get(user=user)
	fav_posts = Post.objects.filter(user=profile)
	fav_posts = []
	favs = request.user.favoritepost_set.all()
	for fav in favs:
		fav_posts.append(fav.post)

	following = Followers.objects.filter(profile=profile)
	following = [f.me for f in following]
	print(following)
	posts = []
	for f in following:
		ps = Post.objects.filter(user=f)
		for p in ps:
			posts.append(p) 
	context={
		'posts' : posts,
		'fav_posts': fav_posts,
	}
	return render(request, 'home.html', context)

def profile(request,profile_id):
	me =  Profile.objects.get(user=request.user)
	profile = Profile.objects.get(id=profile_id)
	posts = Post.objects.filter(user=profile)
	fav_posts = Post.objects.filter(user=profile)
	fav_posts = []
	favs = request.user.favoritepost_set.all()
	for fav in favs:
		fav_posts.append(fav.post)
	my_favs = FavoritePost.objects.filter(user=request.user)
	my_favs = [p.post for p in my_favs]
	following = Follow.objects.filter(profile=profile)
	followers = Followers.objects.filter(profile=profile)
	if(len(Followers.objects.filter(me=profile, profile=me))>0):
		iexist = True
	else:
		iexist = False
	if(me==profile):
		is_my_profile = True
	else:
		is_my_profile = False
	context={
		'profile': profile,
		'posts' : posts,
		'fav_posts': fav_posts,
		'following': following,
		'followers': followers,
		'iexist':iexist,
		'is_my_profile':is_my_profile,
		'my_favs':my_favs,
	}
	return render(request, 'profile.html', context)

def signup(request):
	form = UserForm()
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			profile = Profile.objects.create(user=user)
			profile.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			authen = authenticate(username=username,password=password)
			if authen is not None:
				login(request, authen)
				return redirect('update_profile',profile_id=profile.id)
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

def create_post(request,profile_id):
	my_post = CreatePostForm()
	profile_obj = Profile.objects.get(id=profile_id)
	if request.method == 'POST':
		my_post = CreatePostForm(request.POST, request.FILES or None)
		if my_post.is_valid():
			my_post = my_post.save(commit=False)
			my_post.user = profile_obj
			my_post.save()
			return redirect('profile',profile_id=profile_id)
	context={
		'create_form': my_post,
		'profile_obj' : profile_obj,
	}
	return render(request, 'create_post.html', context)
	# if(request.user.is_anonymous):
	# 		return redirect('login')
	# user = User.objects.get(id=request.user.id)
	# form = CreatePostForm()
	# if request.method == "POST":
	# 	form = CreatePostForm(request.POST, request.FILES or None)
	# 	if form.is_valid():
	# 		form.save(commit=False)
	# 		print(user)
	# 		form.user = user
	# 		form.save()
	# 		return redirect("home")
	# context = {
	# "create_form": form,
	# }
	# return render(request, 'create_post.html', context)


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

def search_profile(request):
	query = request.GET.get("q")
	profiles = Profile.objects.all()
	if query:
		profiles = profiles.filter(user__username__contains=query)
	context = {
	'profiles': profiles,
	}
	return render(request, 'search_profile.html', context)

def follow(request, profile_id):
	me = Profile.objects.get(user=request.user)
	profile = Profile.objects.get(id=profile_id)
	follow_obj, created = Follow.objects.get_or_create(profile=profile,me=me)
	follower_obj, created_ = Followers.objects.get_or_create(profile=me,me=profile)
	if created:
		action = 'follow'
	else:
		action = 'unfollow'
		follow_obj.delete()
		follower_obj.delete()
	# followers_count = len(Followers.objects.filter(profile=profile))
	followers_count = Follow.objects.filter(profile=profile).count()
	#followers_count = Followers.objects.filter(profile=profile)
	response = {
		"action": action,
		'followers_count': followers_count,
	}
	return JsonResponse(response, safe=False)

def delete(request, post_id, profile_id):
	profile = Profile.objects.get(id=profile_id)
	delete_obj= Post.objects.get(id=post_id)
	delete_obj.delete()
	return redirect('profile', profile_id)
	# if()
	# if(not(request.user.is_staff) or request.user==delete_obj.user):
	# 	return redirect





