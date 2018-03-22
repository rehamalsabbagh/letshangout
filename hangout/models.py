from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User , on_delete=models.CASCADE)
	profile_image = models.ImageField(default='none.png')
	profile_bio = models.TextField(max_length=300, null=True)
	# following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="who_follows")
	# followers = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="who_is_followed")

	def __str__(self):
		return self.user.username

class Post(models.Model):
	image = models.ImageField()
	caption = models.TextField()
	user = models.ForeignKey(Profile , on_delete=models.CASCADE)

	def __str__(self):
		return self.caption

class Follow(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='who_is_followed')
	me = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='who_follows')

class Followers(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='who_followss')
	me = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='who_is_followedd')


class FavoritePost(models.Model):
	user = models.ForeignKey(User , on_delete=models.CASCADE)
	post = models.ForeignKey(Post , on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username
