from surprise import Dataset
from surprise import Reader
from surprise.model_selection import train_test_split
from surprise import SVD
import pandas as pd
import datetime

from events import models


class SvdRec:
    user_id = None

    def __init__(self, user_id):
        self.user_id = user_id

    def get_recommendation_qs(self):
        if self.user_id is not None:
            reader = Reader(rating_scale=(1, 5))
            df = pd.DataFrame(list(models.EventUserRating.objects.all().values(
                'user_id', 'event_id', 'rating')))
            data = Dataset.load_from_df(df, reader)

            trainset, testset = train_test_split(data, test_size=0.2)

            algo = SVD()
            algo.fit(trainset)

            lst = []
            for event in models.Event.objects.filter(time_end__gt=datetime.datetime.now()):
                predicted_rating = algo.predict(self.user_id, event.pk)
                lst.append((predicted_rating, event.pk))

            if len(lst) > 0:
                lst.sort(key=lambda x: x[0].est)
                lst.reverse()

                qs = models.Event.objects.filter(
                    id__in=[i[1] for i in lst])[:4]

                return qs
            else:
                return models.Event.objects.filter(time_end__gt=datetime.datetime.now())
        else:
            return models.Event.objects.filter(time_end__gt=datetime.datetime.now())
