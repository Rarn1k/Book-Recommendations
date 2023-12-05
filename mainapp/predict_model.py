import os
import django
import pickle
import pandas as pd
import root.settings as settings
from datetime import datetime
from surprise import Dataset, Reader, KNNBasic
from collections import defaultdict

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
django.setup()

from mainapp.models import UserRating


def create_update_model_predict():
    """
    Create or update user-based collaborative filtering model
    """
    users = list(UserRating.objects.values_list('user', flat=True))
    books = list(UserRating.objects.values_list('book', flat=True))
    ratings = list(UserRating.objects.values_list('book_rating', flat=True))
    df = pd.DataFrame({
        'user_id': users,
        'book_id': books,
        'rating': ratings
    })
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'book_id', 'rating']], reader)
    trainset = data.build_full_trainset()
    sim_opts = {
        'name': 'cosine',
        'user_based': True
    }
    model = KNNBasic(sim_options=sim_opts)
    model.fit(trainset)
    testset = trainset.build_anti_testset()
    print('start prediction', datetime.now())
    predictions = model.test(testset)
    print('end prediction', datetime.now())

    predictions_users = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        predictions_users[uid].append((iid, est))
    path = os.path.join(settings.STATICFILES_DIRS[0], 'model_surprise', 'prediction.pickle')

    with open(path, 'wb') as file:
        pickle.dump(predictions_users, file)


if __name__ == "__main__":
    create_update_model_predict()
