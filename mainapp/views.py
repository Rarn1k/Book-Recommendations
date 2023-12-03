from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Book, Genre
from .handling import get_top_books_genre


def index(request):
    return render(request, 'mainapp/index.html')

@ensure_csrf_cookie
def genre_books(request, genre):

    books = Genre.objects.get(name=genre.lower()).book.all()
    books_res = get_top_books_genre(books)
    books_response = Book.objects.filter(title__in=books_res)
    context = {
        "genre": genre.capitalize(),
        "genre_topbooks": books_response,
    }
    return render(request, "mainapp/genre.html", context)


def book_summary(request):
    book_id = request.POST.get("id", None)
    book = Book.objects.filter(id=book_id.lower())
    summary = book.description
    return JsonResponse({"success": True, "booksummary": summary}, status=200)
