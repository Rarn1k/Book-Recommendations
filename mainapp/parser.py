import os
import pandas as pd
import django
import root.settings as settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
django.setup()

from mainapp.models import Book, Genre


def parse_genres(dfbook):
    genres = [genres.split(',') for genres in dfbook['genre'].unique()]
    flattened_genres = [genre.replace(" ", "") for sublist in genres for genre in sublist]
    finally_genres = list(set(flattened_genres))
    for genre in finally_genres:
        Genre.objects.create(name=genre)


def parse_books(dfbook):
    for i in range(dfbook.shape[0]):
        book_obj = Book.objects.create(title=dfbook['original_title'].iloc[i],
                                       authors=dfbook['authors'].iloc[i],
                                       image_url=dfbook['image_url'].iloc[i],
                                       average_rating=dfbook['average_rating'].iloc[i],
                                       rating_counts=dfbook['ratings_count'].iloc[i],
                                       description=dfbook['desc'].iloc[i])
        genres = dfbook['genre'].iloc[i].split(',')
        genres = [g.replace(" ", "") for g in genres]
        for genre in genres:
            genre_obj, created = Genre.objects.get_or_create(name=genre)
            book_obj.genre.add(genre_obj)


if __name__ == "__main__":

    book_path = os.path.join(settings.STATICFILES_DIRS[0], 'dataset', 'books.csv')
    dfbook = pd.read_csv(book_path)
    Book.objects.all().delete()
    Genre.objects.all().delete()
    parse_genres(dfbook)
    parse_books(dfbook)
