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
        return '%s' % (self.term_content,)

class Clue(models.Model):
    clue_content = models.CharField(max_length = 200)
    term         = models.ForeignKey(Term,related_name='clues')
    clue_number  = models.IntegerField()

    def __unicode__(self):
        return 'Term: %s, Clue: %s, Number: %s' %(self.term,self.clue_content,self.clue_number)

    def get_next(self):
        clues = Clue.objects.filter(clue_number__gt=self.clue_number).order_by('clue_number')
        if clues: return clues[0]
