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

    def all_have_played(self):
        turns = Turn.objects.filter(active_turn__id=self.id)
        for turn in turns:
            if not turn.guess: return False
        return True

    def has_right_answer(self):
        turns = Turn.objects.filter(active_turn__id=self.id)
        correct_answer = self.clue.clue_content
        for turn in turns:
            if turn.guess == correct_answer:
                return True

class Turn(models.Model):
    player_game = models.ForeignKey(Player_Game)
    guess     = models.CharField(max_length=200,blank=True,null=True)
    score     = models.IntegerField(blank=True,null=True)
    active_turn = models.ForeignKey(Active_Turn)

