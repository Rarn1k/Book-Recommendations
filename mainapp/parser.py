import os
import pandas as pd
import django
import random
import string
import root.settings as settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
django.setup()

from mainapp.models import Book, Genre, UserRating, User


def parse_genres(dfbook):
    """
    Filling out the table Genre from dataset.

    Parameters:
    -----------
    dfbook: pd.DataFrame
        Dataset with books
    """
    genres = [genres.split(',') for genres in dfbook['genre'].unique()]
    flattened_genres = [genre.replace(" ", "") for sublist in genres for genre in sublist]
    finally_genres = list(set(flattened_genres))
    for genre in finally_genres:
        Genre.objects.create(name=genre)


def parse_books(dfbook):
    """
    Filling out the table Book from dataset.

    Parameters:
    -----------
    dfbook: pd.DataFrame
        Dataset with books
    """
    for i in range(dfbook.shape[0]):
        book_obj = Book.objects.create(id=dfbook['r_index'].iloc[i],
                                       title=dfbook['original_title'].iloc[i],
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


def parse_ratings(dfratings):
    """
    Filling out the tables USer and UserRating from dataset (first 500 users).

    Parameters:
    -----------
    dfbook: pd.DataFrame
        Dataset with books
    """
    users_id = dfratings['user_id'].unique()
    users_id = sorted(users_id)
    new_dfratings = dfratings[dfratings['user_id'] < users_id[500]]
    filtered_users = new_dfratings['user_id'].unique()
    for user_id in filtered_users:
        letters = string.ascii_lowercase
        rand_name = ''.join(random.choice(letters) for i in range(6))
        try:
            user_obj = User.objects.get(id=user_id) #если пользователь в базе есть
        except:
            user_obj = User.objects.create_user(id=user_id, username=rand_name) #создаем с рандомным логином
        user_ratings = new_dfratings[new_dfratings['user_id'] == user_id]
        for i in range(user_ratings.shape[0]):
            try:
                book = Book.objects.get(id=user_ratings['book_id'].iloc[i])
                UserRating.objects.create(user=user_obj,
                                          book=book,
                                          book_rating=user_ratings['rating'].iloc[i])
            except:
                continue
    print('')


if __name__ == "__main__":

    book_path = os.path.join(settings.STATICFILES_DIRS[0], 'dataset', 'books.csv')
    rating_path = os.path.join(settings.STATICFILES_DIRS[0], 'dataset', 'ratings.csv')
    dfbook = pd.read_csv(book_path)


    ##----parse genres----
    # Genre.objects.all().delete()
    # parse_genres(dfbook)


    ##----parse books----
    # Book.objects.all().delete()
    # parse_books(dfbook)


    ## ----parse ratings----
    # dfratings = pd.read_csv(rating_path)
    # parse_ratings(dfratings)

