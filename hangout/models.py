from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User , on_delete=models.CASCADE)
	profile_image = models.ImageField(default='none.png')
	profile_bio = models.TextField(max_length=25)

	def __str__(self):
		return self.user.username

class Post(models.Model):
	image = models.ImageField()
	caption = models.TextField()
	user = models.ForeignKey(Profile , on_delete=models.CASCADE)

	def __str__(self):
		return self.caption

class Favorite(models.Model):
	user = models.ForeignKey(User , on_delete=models.CASCADE)
	post = models.ForeignKey(Post , on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

class Follow(models.Model):
      following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_follows")
      follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_is_followed")