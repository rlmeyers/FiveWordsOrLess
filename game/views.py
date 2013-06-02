from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from player.models import Player, Player_Game, Turn, Active_Turn
from term.models import Genre
from django import forms
from game.models import Game
from django.utils import timezone
from game.helpers import activate_game
from django.db.models import Q
from term.helpers import get_next_term

def new(request):
    if request.method == 'GET':
        return render(request, 'player/new.html',{})
    elif request.method == 'POST':
        if request.POST['name'] == '':
            return render(request,'player/new.html',{'error':'You must have a username'})
        else:
            player = Player(name = request.POST['name'])
            player.save()
            return HttpResponseRedirect('/player/%s/' % player.id)


def home(request):
    players = Player.objects.all()
    return render(request,'player/index.html',{'players':players})

def detail(request,pk):
    game = Game.objects.get(pk=pk)
    return render(request,'game/detail.html',{'game':game})

def new_game(request,pk):
    if request.method=='GET':
        player = Player.objects.get(pk=pk)
        players = Player.objects.all()
        genres  = Genre.objects.all()
        return render(request,'player/new_game.html',{'players':players,'genres':genres,'player':player})
    else:
        print '## Adding New Game ##'
        game = Game(name = request.POST['name'],date = timezone.now(),active=False)
        game.save()
        print '## Saved Game ID: %s with name %s ##' % (game.id,game.name)
        player = Player.objects.get(pk=pk)
        PG = Player_Game(game = game, player = player, score = 0,accepted = True, declined = False)
        print '## The first player in the game is %s with ID %s ##' % (player.name, player.id)
        PG.save()
        players = request.POST.getlist('players')
        for p in players:
            player = Player.objects.get(pk = int(p))
            PG = Player_Game(game = game, player = player, score = 0, accepted = False, declined = False)
            PG.save()
            print '## Player %s with ID %s was invited to this game ##' % (player.name,player.id)

        return HttpResponse("Well we found a post to /player/%s/game/new/"%pk)

def player_game(request,gpk,ppk):
    if request.method=="POST":
        print '## This is a Post ##'
        pg = Player_Game.objects.get(player__id=ppk,game__id=gpk)
        pg.accepted = True if request.POST['submit']=='accept' else False
        pg.declined = True if request.POST['submit']=='decline' else False
        print '## The game has been %s by player %s ##' % (('accepted' if pg.accepted else 'declined'),pg.player.name)
        pg.save()
        player_games = Player_Game.objects.filter(game__id = gpk)
        all_true = True
        for pg in player_games:
            if not (pg.accepted or pg.declined):
                all_true = False
                print '## Player %s with id %s has not yet accepted game %s with id %s ##' %(pg.player.name, pg.player.id, pg.game.name, pg.game.id)
        if all_true:
            game = Game.objects.get(pk=gpk)
            game.active = True
            game.save()
            activate_game(game.id)
            print '## Set Game %s with ID %s to active ##' % (game.name,game.id)
        return HttpResponseRedirect("/player/%s/"%ppk)
    else:
        game = Game.objects.get(pk=gpk)
        player = Player.objects.get(pk=ppk)
        print '## We are checking out game %s with ID %s ##' % (game.name,game.id)
        current_clue = None
        turns = None
        player_turns  = Turn.objects.filter(Q(active_turn__active=True, player_game__player__id=ppk, player_game__game__id=gpk))
        for player_turn in player_turns:
            print 'Player Turn: guess: %s part of game: %s by player: %s and is_active: %s and is on term: %s' % (player_turn.guess, player_turn.player_game.game.name,player_turn.player_game.player.name,player_turn.active_turn.active,player_turn.active_turn.clue.clue_content)
        print 'There were %s turns in the database' % len(player_turns)
        player_turn = player_turns[0]
        print 'The guess in the database was %s' % player_turn.guess
        current_clues = game.active_turn_set.filter(active=True)
        current_clue = current_clues[0] if len(current_clues)==1 else None
        turns = Turn.objects.filter(Q(player_game__player__id=ppk,player_game__game__id=gpk, active_turn__clue__term__id=current_clue.clue.term.id,guess__isnull=False)).order_by('active_turn__clue__clue_number')
        print '## We found these turns %s ##' % ', '.join([str(turn) for turn in turns])
        return render(request,'game/player_game.html',{'current_clue':current_clue.clue,'turns':turns,'game':game,'player':player})


def submit(request,gpk,ppk):
    if request.method=="POST":
        game = Game.objects.get(pk=gpk)
        player_games = Player_Game.objects.filter(Q(game__id=gpk,player__id=ppk))
        if len(player_games)>0:
            player_game = player_games[0]
            player_turn = Turn.objects.filter(Q(active_turn__active=True, player_game__player__id=ppk, player_game__game__id=gpk))[0]
            player_turn.guess = 'PASS' if request.POST.has_key('pass') else request.POST['answer']
            player_was_correct = player_turn.guess == player_turn.active_turn.clue.term.term_content
            print '## The Player Guessed %s for the term %s ##' % (player_turn.guess,player_turn.active_turn.clue.term.term_content,)
            player_turn.save()
            all_have_played = player_turn.active_turn.all_have_played()
            print '## All the players have played ##' if all_have_played else '## Still waiting on players ##'
            has_right_answer =  player_turn.active_turn.has_right_answer()
            if has_right_answer:
                print '## Someone got the answer right ##'
            else:
                print '## No one got the answer right ##'
            if all_have_played:
                clue = None
                if has_right_answer:
                    print '## We need a new term ##'
                else:
                    print '## We need a new clue ##'
                    clue = player_turn.active_turn.clue.get_next()
                if not clue:
                    print '## The term have no clues left ##'
                    clue = get_next_term(gpk)
                    if not clue:
                        game.active = False
                        game.save()
                        return HttpReponse("There were no more terms in the database")
                AT = player_turn.active_turn
                AT.active = False
                AT.save()
                AT = Active_Turn(game=game,clue = clue,active=True)
                AT.clue = clue
                AT.save()
                user_games = Player_Game.objects.filter(Q(game__id=gpk))
                for ug in user_games:
                    turn = Turn(player_game = ug, active_turn=AT)
                    turn.save()

            active_games   = Game.objects.filter(Q(active=True,player_game__accepted=True, player_game__player__id=ppk,player_game__turn__active_turn__active=True,player_game__turn__guess=None))
            inactive_games = Game.objects.filter(Q(active=False,player_game__accepted=True, player_game__player__id=ppk)|Q(active=True,player_game__accepted=True,player_game__player__id=ppk,player_game__turn__active_turn__active=True,player_game__turn__guess__isnull=False))
            new_games      = Game.objects.filter(Q(active__exact=False,player_game__player__id=ppk,player_game__accepted=False,player_game__declined=False))
            return render(request,'player/detail.html',{'message':('You were correct' if player_was_correct else 'You were incorrect'),'active_games':active_games,'inactive_games':inactive_games,'new_games':new_games})
        else:
            return HttpResponse("Something went wrong.  There were %s player_games found in the database for player %s" %(len(player_games),ppk))
    else:
        return HttpResponseRedirect("/game/%s/player/%s/" % (gpk,ppk,))
