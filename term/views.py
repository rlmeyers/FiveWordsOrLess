from django.shortcuts import render
from django.http import HttpResponseRedirect
from term.models import TermForm

def new(request):
    if request.method == 'GET':
        form = TermForm()
        return render(request, 'term/new.html', {'form', form})
