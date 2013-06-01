from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from player.models import Player

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
