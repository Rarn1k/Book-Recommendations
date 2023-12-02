from django.shortcuts import render
from .models import Book, Genre
from .handling import get_top_books_genre


def index(request):
    return render(request, 'mainapp/index.html')


def genre_books(request, genre):

    books = Genre.objects.get(name=genre.lower()).book.all()
    books_res = get_top_books_genre(books)
    books_response = Book.objects.filter(title__in=books_res)
    context = {
        "genre": genre.capitalize(),
        "genre_topbooks": books_response,
    }
    return render(request, "mainapp/genre.html", context)
