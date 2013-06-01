from django.db import models
from django import forms

class Genre(models.Model):
    genre_name   = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.genre_name

class Term(models.Model):
    term_content = models.CharField(max_length = 200)
    genres       = models.ManyToManyField(Genre)

    def __unicode__(self):
        return self.term_content

class Clue(models.Model):
    clue_content = models.CharField(max_length = 200)
    term         = models.ForeignKey(Term)
    clue_number  = models.IntegerField()
