from django.urls import path

from . import views_ajax
from .views import index, genre_books, book_summary, explore_books, personal_recommendations, saved_list, rated_books

urlpatterns = [
    path('', index, name='index'),
    path("genre_books/<genre>", genre_books, name="genre_books"),
    path("book_summary/", book_summary, name="summary"),
    path("explore_books/", explore_books, name="explore_books"),
    path("personal_recommendations/", personal_recommendations, name="personal_recommendations"),
    path("saved_list/", saved_list, name="saved_list"),
    path("rated_books/", rated_books, name="rated_books"),
]


urlpatterns += [
    path("search_ajax/", views_ajax.search, name="search_ajax"),
    path("book_details_ajax/", views_ajax.get_book_details, name="book_details"),
    path("user_rate_book/", views_ajax.user_rate_book, name="user_rate_book"),
    path("save_book/", views_ajax.save_book, name="save_book"),
    path("remove_saved_book/", views_ajax.remove_saved_book, name="remove_saved_book"),
]