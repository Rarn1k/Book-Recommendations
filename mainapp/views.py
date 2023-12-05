from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Book, Genre, UserRating
from .handling import get_top_books, get_popular_among_users, get_predictions, get_recommendations_for_user
from .predict_model import create_update_model_predict


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


@login_required
@ensure_csrf_cookie
def personal_recommendations(request):
    current_user = request.user
    user_ratings = list(UserRating.objects.filter(user=current_user))
    if len(user_ratings) < 5:
        messages.info(request, "Для ваших личных рекомендаций оцените как минимум 5 книг")
        return redirect("index")
    predictions = get_predictions()
    if current_user.id not in predictions:
        create_update_model_predict()
        predictions = get_predictions()
    n = 10
    if current_user.id in predictions:
        top_books_n = get_recommendations_for_user(current_user.id, predictions, n)
        id_books = [x[0] for x in top_books_n]
        books = Book.objects.filter(id__in=id_books)
        context = {
            "books": books,
            "n": n
        }
        return render(request, "mainapp/recommendations.html", context=context)


