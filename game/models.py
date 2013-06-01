from django.db import models
from term.models import Genre

class Game(models.Model):
    date   = models.DateField()
    genres = models.ManyToManyField(Genre)
    name   = models.CharField(max_length=200)

