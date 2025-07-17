from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	date = models.DateField()
	time = models.TimeField()
	location = models.TextField()
	category = models.ForeignKey("Category", on_delete=models.CASCADE, default=1)
	participant = models.ManyToManyField(User, related_name="rsvp_events")
	evn_img = models.ImageField(upload_to='event_img', blank=True, null=True, default='event_img/default_img.jpg')

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()

	def __str__(self):
		return self.name

