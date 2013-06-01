from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from player.models import Player, Player_Game
from term.models import Genre
from django import forms
from game.models import Game
from django.utils import timezone

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
    player = Player.objects.get(pk=pk)
    return render(request,'player/detail.html',{'player':player})

def new_game(request,pk):
    if request.method=='GET':
        player = Player.objects.get(pk=pk)
        players = Player.objects.all()
        genres  = Genre.objects.all()
        return render(request,'player/new_game.html',{'players':players,'genres':genres,'player':player})
    else:
        print '## Adding New Game ##'
        game = Game(name = request.POST['name'],date = timezone.now())
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

class NewGameForm(forms.Form):
    name = forms.CharField(max_length=200)
    genres = forms.ModelMultipleChoiceField(Genre.objects.all())
    players = forms.ModelMultipleChoiceField(Player.objects.all())
