from django.shortcuts import render
from django.http import HttpResponseRedirect


def index(request):
    return render(request, 'mainapp/index.html')


def genre_books(request, genre):
    return HttpResponseRedirect('/')