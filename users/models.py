from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
	profile_image = models.ImageField(upload_to='profile_image',blank=True, default='profile_image/default_img.jpg')
	phone = models.CharField(blank=True, ) 

	def __str__(self):
		return self.username