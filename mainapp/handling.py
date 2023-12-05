import os
import random
import operator
import pandas as pd
import pickle
import root.settings as settings


def get_top_books(books):
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


def get_popular_among_users(all_ratings, books, n):
    random.shuffle(all_ratings)
    best_users_ratings = sorted(all_ratings, key=operator.attrgetter("book_rating"), reverse=True)
    filtered_books = set()
    # for i, rating in enumerate(best_users_ratings):
    #     if rating.book_rating >= 4:
    #         filtered_books.add(rating.book.id)
    #     elif rating.book_rating < 4 or len(filtered_books) == n:
    #         break

    remaining_books = n - len(filtered_books)
    if remaining_books >= 0:
        rem_books = get_top_books(books)['id'].head(2 * n).sample(2 * n).tolist()
        filtered_books = (
                list(filtered_books)
                + list(set(rem_books) - filtered_books)[:remaining_books]
        )
    return filtered_books


def get_predictions():

    path = os.path.join(settings.STATICFILES_DIRS[0], 'model_surprise', 'prediction.pickle')
    try:
        with open(path, 'rb') as file:
            predictions = pickle.load(file)
    except OSError as e:
        print(e)
        predictions = []

    return predictions


def get_recommendations_for_user(user_id, predictions, n):

    user_ratings = predictions[user_id]
    user_ratings.sort(key=lambda x: x[1], reverse=True)

    return user_ratings[:n]








