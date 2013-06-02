from game.models import Game
from term.models import Term
from player.models import Active_Turn, Turn, Clue, Player_Game
from django.db.models import Q

def activate_game(gpk):
    game = Game.objects.get(pk=gpk)
    print '## Activating Game %s with ID %s ##' %(game.name,game.id)
    terms = Term.objects.filter(Q(genres__genre_name__in=[str(g.genre_name) for g in game.genres.all()]))
    t = terms[0]
    c = t.clues.all().order_by('clue_number')[0]
    AT = Active_Turn(active=True,game=game,clue=c)
    AT.save()
    user_games = Player_Game.objects.filter(Q(game__id=gpk))
    for user_game in user_games:
        turn = Turn(player_game=user_game,active_turn=AT)
        turn.save()

