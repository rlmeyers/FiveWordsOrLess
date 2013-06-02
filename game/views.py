from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from player.models import Player, Player_Game, Turn
from term.models import Genre
from django import forms
from game.models import Game
from django.utils import timezone
from game.helpers import activate_game
from django.db.models import Q

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
        player_turn  = Turn.objects.filter(Q(active_turn__active=True, player_game__player__id=ppk, player_game__game__id=gpk))[0]
        current_clue = game.active_turn.clue if not player_turn.guess else None
        turns = Turn.objects.filter(Q(player_game__player__id=ppk,player_game__id=gpk, active_turn__clue__term__id=game.active_turn.clue.term.id,guess__isnull=False)).order_by('active_turn__clue__clue_number')
        print '## We found these turns %s ##' % ', '.join([str(turn) for turn in turns])
        return render(request,'game/player_game.html',{'current_clue':current_clue,'turns':turns,'game':game,'player':player})


def submit(request,gpk,ppk):
    if request.method=="POST":
        player_games = Player_Game.objects.filter(Q(game__id=gpk,player__id=ppk))
        if len(player_games)>0:
            player_game = player_games[0]
            player_turn = Turn.objects.filter(Q(active_turn__active=True, player_game__player__id=ppk, player_game__game__id=gpk))[0]
            player_turn.guess = 'PASS' if request.POST.has_key('pass') else request.POST['answer']
            print '## The Player Guessed %s for the term %s ##' % (player_turn.guess,player_turn.active_turn.clue.term.term_content,)
            player_turn.save()
            return HttpResponse("You were %s" % ("Correct" if player_turn.guess == player_turn.active_turn.clue.term.term_content else "Incorrect"))
        else:
            return HttpResponse("Something went wrong.  There were %s player_games found in the database for player %s" %(len(player_games),ppk))
    else:
        return HttpResponseRedirect("/game/%s/player/%s/" % (gpk,ppk,))
