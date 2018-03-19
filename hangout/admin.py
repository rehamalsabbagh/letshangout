from django.contrib import admin
from .models import Profile, Post, Favorite, Follow

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Favorite)
admin.site.register(Follow)
# Register your models here.
