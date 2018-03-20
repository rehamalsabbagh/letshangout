from django.contrib import admin
from .models import Profile, Post, FavoritePost, Follow

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(FavoritePost)
admin.site.register(Follow)
# Register your models here.
