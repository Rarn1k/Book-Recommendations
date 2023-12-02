import pandas as pd


def get_top_books_genre(books):
    books_data = list(books.values())
    dfbook = pd.DataFrame.from_records(books_data)

    v = dfbook['rating_counts']
    m = dfbook['rating_counts'].quantile(0.85)
    R = dfbook['average_rating']
    C = dfbook['average_rating'].mean()
    W = (R * v + C * m) / (v + m)
    dfbook = dfbook.assign(weighted_rating=W)
    dfbook.sort_values("weighted_rating", ascending=False, inplace=True)

    books_res = dfbook['title'].head(48).sample(16).values
    return books_res
