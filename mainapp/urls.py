from django.urls import path
from .views import index, genre_books

urlpatterns = [
    path('', index, name='index'),
    path("genre_books/<genre>", genre_books, name="genre_books"),
]
