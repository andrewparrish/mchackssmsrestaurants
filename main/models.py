from django.db import models

# Create your models here.
class Directions(models.Model):
	phone = models.CharField(max_length=200, blank=True)
	directions = models.CharField(max_length=400, blank=True)
	location = models.CharField(max_length=400, blank=True)
