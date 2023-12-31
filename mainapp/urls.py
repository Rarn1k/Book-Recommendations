from django.urls import path, re_path

from . import views_ajax
from .views import index, explore_books, personal_recommendations, saved_list, rated_books

urlpatterns = [
    path('', index, name='index'),
    path("explore_books/", explore_books, name="explore_books"),
    path("personal_recommendations/", personal_recommendations, name="personal_recommendations"),
    path("saved_list/", saved_list, name="saved_list"),
    path("rated_books/", rated_books, name="rated_books"),

    re_path(r'^explore_books/$', explore_books, name='explore_books_with_params'),
]


urlpatterns += [
    path("search_ajax/", views_ajax.search, name="search_ajax"),
    path("book_details_ajax/", views_ajax.get_book_details, name="book_details"),
    path("user_rate_book/", views_ajax.user_rate_book, name="user_rate_book"),
    path("save_book/", views_ajax.save_book, name="save_book"),
    path("remove_saved_book/", views_ajax.remove_saved_book, name="remove_saved_book"),
    path("check_saved_book/", views_ajax.check_saved_book, name="check_saved_book")
]
