from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from term.models import Genre, Term, Clue
from django.template import RequestContext

def new(request):
    if request.method == 'GET':
        return render(request, 'term/new.html',{})
    elif request.method == 'POST':
        context = {}
        try:
            genre = Genre.objects.get(genre_name=request.POST['genre'])
        except:
            genre = Genre(genre_name=request.POST['genre'])
            genre.save()
            print 'Saved Genre: %s' % str(genre)
        if request.POST['term'] == '':
            return render(request,"term/new.html",{'error':'You must have a term name'})
        term = Term(term_content = request.POST['term'])
        term.save()
        term.genres.add(genre)
        print 'Saved Term: %s' % str(term)
        n = 0
        clues = ['clue_1','clue_2','clue_3','clue_4','clue_5']
        cs = []
        for c in clues:
            if request.POST[c] != '':
                clue = Clue(clue_content=request.POST[c], term = term, clue_number = n)
                cs.append(request.POST[c])
                n += 1
                clue.save()
                print 'Saved Clue: %s' % str(clue)
        return render(request,'term/submitted.html',{'genre':request.POST['genre'],'clues':cs,'term':request.POST['term']})


def home(request):
    terms = Term.objects.all()
    return render(request,'term/index.html',{'terms':terms})

def detail(request,pk):
    term = Term.objects.get(pk=pk)
    clues = term.clues.all()
    genres = term.genres.all()
    return render(request,'term/detail.html',{'term':term,'clues':clues,'genres':genres})
