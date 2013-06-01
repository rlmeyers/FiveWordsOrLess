from django.db import models
from game.models import Game
from term.models import Clue

class Player(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Player_Game(models.Model):
    player = models.ForeignKey(Player)
    game   = models.ForeignKey(Game)
    score  = models.IntegerField()
    current_clue = models.ForeignKey(Clue)
    accepted = models.BooleanField()
    declined = models.BooleanField()
