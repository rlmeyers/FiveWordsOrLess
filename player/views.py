from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from player.models import Player
from term.models import Genre
from django import forms

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
        form = NewGameForm()
        form.players = forms.ModelMultipleChoiceField(Player.objects.filter())
        return render(request,'player/new_game.html',{'form':form,'player':player})
    else:
        print '## Adding New Game ##'
        for key in request.POST.keys():
            print key,request.POST[key]
        return HttpResponse("Well we found a post to /player/%s/game/new/"%pk)

class NewGameForm(forms.Form):
    name = forms.CharField(max_length=200)
    genres = forms.ModelMultipleChoiceField(Genre.objects.all())
    players = forms.ModelMultipleChoiceField(Player.objects.all())
