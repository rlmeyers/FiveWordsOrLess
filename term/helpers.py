from game.models import Game
from term.models import Term
from django.db.models import Q

def get_next_term(gpk):
    game = Game.objects.get(pk=gpk)
    terms = Term.objects.filter(Q(genres__genre_name__in=[str(g.genre_name) for g in game.genres.all()]))
    if terms:
        t = terms[0]
        c = t.clues.all().order_by('clue_number')[0]
        return c
    return None

