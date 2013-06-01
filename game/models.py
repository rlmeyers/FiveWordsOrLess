from django.db import models
from term.models import Genre, Clue

class Game(models.Model):
    date   = models.DateField()
    genres = models.ManyToManyField(Genre)
    name   = models.CharField(max_length=200)
    active = models.BooleanField()
    current_clue = models.ForeignKey(Clue,null=True,blank=True)

