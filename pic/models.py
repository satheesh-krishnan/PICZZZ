from django.db import models
from django.contrib.auth.models import User
import datetime


class UserProfile(models.Model):
	user_id = models.OneToOneField(User)
	profile_picture = models.ImageField(upload_to='profile', blank=True)
	
class Photos(models.Model):
	upload_photo = models.ImageField(upload_to='photo',blank=True)
	user_id = models.ForeignKey(User)
	views = models.IntegerField(default=0)
	follows = models.IntegerField(default=0)
	comments_num = models.IntegerField(default=0)
	date_time = models.DateTimeField(default=datetime.datetime.now)
	

class PhotoFollows(models.Model):
	user_id = models.ForeignKey(User)
	photo_id = models.ForeignKey(Photos)


class UserFollows(models.Model):
	from_user = models.CharField(max_length=128)
	to_user = models.CharField(max_length=128)

class Comments(models.Model):
	user_id = models.ForeignKey(User)
	photo_id = models.ForeignKey(Photos)
	date_time = models.DateTimeField(default=datetime.datetime.now)
