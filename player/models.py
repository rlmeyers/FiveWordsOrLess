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
    accepted = models.BooleanField()
    declined = models.BooleanField()

class Active_Turn(models.Model):
    active  = models.BooleanField()
    clue    = models.ForeignKey(Clue)
    game    = models.ForeignKey(Game)

class Turn(models.Model):
    player_game = models.ForeignKey(Player_Game)
    guess     = models.CharField(max_length=200,blank=True,null=True)
    score     = models.IntegerField(blank=True,null=True)
    active_turn = models.ForeignKey(Active_Turn)

