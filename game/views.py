from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from player.models import Player, Player_Game
from term.models import Genre
from django import forms
from game.models import Game
from django.utils import timezone
from game.helpers import activate_game

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
    return HttpResponse("Well we are here")
