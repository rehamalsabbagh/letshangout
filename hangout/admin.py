from django.contrib import admin
from .models import Profile, Post, FavoritePost, Follow,Followers

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(FavoritePost)
admin.site.register(Follow)
admin.site.register(Followers)
# Register your models here.
