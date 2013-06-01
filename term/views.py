from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from term.models import Genre, Term, Clue

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
        term = Term(term_content = request.POST['term'])
        term.save()
        term.genres.add(genre)
        print 'Saved Term: %s' % str(term)
        n = 0
        clues = ['clue_1','clue_2','clue_3','clue_4','clue_5']
        for c in clues:
            if request.POST[c] != '':
                clue = Clue(clue_content=request.POST[c], term = term, clue_number = n)
                n += 1
                clue.save()
                print 'Saved Clue: %s' % str(clue)
        return HttpResponse('This is a post at /term/new')


def home(request):
    return HttpResponse('This is the home page for terms')
