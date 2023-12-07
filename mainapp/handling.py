import os
import pandas as pd
import pickle
import root.settings as settings
from collections import defaultdict


def get_top_books(books):
    """
    Get top books according to the formula IMDbb (Internet Movie database).
    Books are ordered by weighted average.

    Parameters:
    ___________
    books: QuerySet
        Books from database.
    Return:
    _______
    dfbook: pd.DataFrame
        DataFrame with ordered books.
    """
    books_data = list(books.values())
    dfbook = pd.DataFrame.from_records(books_data)

    v = dfbook['rating_counts']
    m = dfbook['rating_counts'].quantile(0.85)
    R = dfbook['average_rating']
    C = dfbook['average_rating'].mean()
    W = (R * v + C * m) / (v + m)
    dfbook = dfbook.assign(weighted_rating=W)
    dfbook.sort_values("weighted_rating", ascending=False, inplace=True)

    return dfbook


def get_popular_among_users(books, n):
    """
    Get n popular books according to the formula IMDbb (Internet Movie Database).

    Parameters:
    ___________
    books: QuerySet
        Books from database.
    n: int
        Needed count of returns books
    Return:
    _______
    books: pd.DataFrame
        DataFrame with ordered books.
    """
    books = get_top_books(books)['id'].head(2 * n).sample(n).tolist()

    return books


def get_predictions():
    """
    Get ratings predictions from pickle objects.

    Return:
    _______
    predictions: defaultdict(list)
        Rating predictions for all users.
    """
    path = os.path.join(settings.STATICFILES_DIRS[0], 'model_surprise', 'prediction.pickle')
    try:
        with open(path, 'rb') as file:
            predictions = pickle.load(file)
    except OSError as e:
        print(e)
        predictions = defaultdict(list)

    return predictions


def get_recommendations_for_user(user_id, predictions, n):
    """
    Get rating predictions for some user.

    Parameters:
    ___________
    user_id: int
        User ID from Database
    predictions: defaultdict(list)
        Rating predictions for all users
    n: int
        Count of recommended books
    """
    user_ratings = predictions[user_id]
    user_ratings.sort(key=lambda x: x[1], reverse=True)

    return user_ratings[:n]








