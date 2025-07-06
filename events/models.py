from django.db import models


class Participant(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(unique=True, null=True, blank=True)

	def __str__(self):
		return self.name


class Event(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	date = models.DateField()
	time = models.TimeField()
	location = models.TextField()
	category = models.ForeignKey("Category", on_delete=models.CASCADE, default=1)
	participant = models.ManyToManyField(Participant, related_name="event_participant")

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()

	def __str__(self):
		return self.name