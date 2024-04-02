from surprise import Dataset
from surprise import Reader
from surprise.model_selection import train_test_split
from surprise import SVD
from surprise import accuracy
from django.core.management.base import BaseCommand
import pandas as pd

from events import models


class Command(BaseCommand):
    help = "This command testing SVD"

    def handle(self, *args, **options):

        # Преобразование queryset в формат, поддерживаемый scikit-surprise
        reader = Reader(rating_scale=(1, 5))
        df = pd.DataFrame(list(models.EventUserRating.objects.all().values('user_id', 'event_id', 'rating')))
        data = Dataset.load_from_df(df, reader)

        # Разделение данных на тренировочный и тестовый наборы
        trainset, testset = train_test_split(data, test_size=0.2)

        # Используем алгоритм SVD (Singular Value Decomposition)
        algo = SVD()
        algo.fit(trainset)

        # Получение предсказаний для тестового набора
        predictions = algo.test(testset)

        # Оценка точности предсказаний
        accuracy.rmse(predictions)

        # Пример предсказания рейтинга для конкретного пользователя и события
        user_id = 1
        # event_id = 10
        lst = []

        for event in models.Event.objects.all():
            predicted_rating = algo.predict(user_id, event.pk)
            lst.append((predicted_rating, event.pk))

        lst.sort(key=lambda x: x[0].est)
        lst.reverse()
        for i in lst:
            print(i[1], i[0].est)


        self.stdout.write(self.style.SUCCESS(f"Предсказанный рейтинг для пользователя {user_id} и события {lst[0][1]}: {lst[0][0].est}"))
