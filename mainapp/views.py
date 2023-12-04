from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Book, Genre, UserRating
from .handling import get_top_books, get_popular_among_users


def index(request):
    all_ratings = list(UserRating.objects.all().order_by("-book_rating"))
    books = Book.objects.all()
    popular_books_id = get_popular_among_users(all_ratings, books, 15)
    popular_books = Book.objects.filter(id__in=popular_books_id)
    context = {
        'books': popular_books
    }
    return render(request, 'mainapp/index.html', context)

@ensure_csrf_cookie
def genre_books(request, genre):

    books = Genre.objects.get(name=genre.lower()).book.all()
    books_res = get_top_books(books)
    books_res = books_res['title'].head(48).sample(16).values
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


def explore_books(request):
    books = Book.objects.all()
    sample = get_top_books(books)['title'].head(400).sample(152).values
    books_results = Book.objects.filter(title__in=sample)
    return render(request, "mainapp/explore.html", {'books': books_results})

