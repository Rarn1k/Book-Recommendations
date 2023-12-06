from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Book, Genre, UserRating, SaveForLater
from .handling import get_top_books, get_popular_among_users, get_predictions, get_recommendations_for_user
from .predict_model import create_update_model_predict


def index(request):
    books = Book.objects.all()
    popular_books_id = get_popular_among_users(books, 15)
    popular_books = Book.objects.filter(id__in=popular_books_id)
    context = {
        'books': popular_books
    }
    return render(request, 'mainapp/index.html', context)


def book_summary(request):
    book_id = request.POST.get("id", None)
    book = Book.objects.filter(id=book_id.lower())
    summary = book.description
    return JsonResponse({"success": True, "booksummary": summary}, status=200)


def explore_books(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')
    author = request.GET.get('authors', '')
    selected_genre = request.GET.get('genre')

    books = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query)

    if author:
        books = books.filter(authors__icontains=author)

    if selected_genre:
        books = books.filter(genre__name=selected_genre)

    if books:
        if sort_by == "rating":
            sample = get_top_books(books)['title'].values
            books = Book.objects.filter(title__in=sample)
        elif sort_by == 'number_of_ratings':
            books = books.order_by("rating_counts")
        elif sort_by == "title":
            books = books.order_by("title")
        elif sort_by == "authors":
            books = books.order_by("authors")
        else:
            sample = get_top_books(books)['title'].values
            # sample = get_top_books(books)['title'].head(400).sample(152).values
            books = Book.objects.filter(title__in=sample)

    genres = Genre.objects.all()

    context = {
        "books": books[:100],
        "genres": genres,
        "selected_genre": selected_genre,
    }

    return render(request, "mainapp/explore.html", context)


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


def saved_list(request):
    books = SaveForLater.objects.filter(user=request.user).values_list("book", flat=True)
    if not books:
        messages.info(request, "У вас нет сохраненных книг")
        return redirect("index")
    total_books = len(books)
    pag_books = Book.objects.filter(id__in=books)
    paginator = Paginator(pag_books, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "mainapp/saved_books.html", {"page_obj": page_obj, "num": total_books}
    )


def rated_books(request):
    books_ratings = UserRating.objects.filter(user=request.user)
    if not books_ratings:
        messages.info(request, "У вас нет оцененных книг")
        return redirect("index")
    total_books = len(books_ratings)
    paginator = Paginator(books_ratings, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "mainapp/rated_books.html", {"page_obj": page_obj, "num": total_books}
    )
