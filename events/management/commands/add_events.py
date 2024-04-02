import random
from django.utils import timezone
import datetime

from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten

from django_seed import Seed

from users.models import User
from events import models as event_models

events_lst = [
    "Научно-практический семинар Здоровье студентов и условия его сохранения в процессе обучения",
    "ПРАВОВЫЕ И ВЕТЕРИНАРНЫЕ АСПЕКТЫ В КОННОЙ СФЕРЕ",
    "Круглый стол: Инновационные технологии природообустройства",
    "Основы ландшафтного полива",
    "Современные технологии питомниководства России, Европы и США",
    "Цифровизация системы документооборота инвестиционно-строительного проекта с применением смарт-контрактов",
    "Форум уличного искусства Стрит-арт Сибирь",
    "Мастер-класс Генерирование предпринимательской идеи стартап-проекта",
    "Вводная лекция для новичков добровольческого поисково-спасательного отряда ЛизаАлерт Волгоградской области",
    "Лекция в гибридном формате Эволюция вселенной. Нейтронные звёзды",
    "Вебинар: Когда компания 100% способна на большее. Поиск точек роста",
    "Бизнес-нетворкинг Твой запрос",
    "Предпринимательский урок для будущих строителей",
    "Регулярная встреча #143 бизнес-клуба публичных выступлений Optima Forma",
    "Встреча Сообщества Офтальмологов",
    "Тема: Стратегическая встреча по вопросам этики организаторов выпусков биржевых облигаций",
    "Молодежный совет при Уполномоченном по защите прав предпринимателей в городе Москве",
    "Практикум Школы краудфандинга от Фонда поддержки социальных проектов и Planeta.ru",
    "Нейроотличие и РАС: популяризация и возможности психотерапии",
]


class Command(BaseCommand):
    help = "This command creates events"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many events do you want ro create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = User.objects.all()

        seeder.add_entity(event_models.Event, number, {
            "title": lambda x: random.choice(events_lst),
            "price": lambda x: random.randint(1, 500),
            "time_start": datetime.datetime.now(tz=timezone.utc),
            "time_end": lambda x: datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=random.randint(5, 20)),
        })
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        tags = event_models.Tag.objects.all()
        for pk in created_clean:
            event = event_models.Event.objects.get(pk=pk)
            event.preview = f"Photos/{random.randint(1, 10)}.jpg",
            event.save()
            for t in tags:
                rnd_number = random.randint(1, 15)
                if rnd_number % 2 == 0:
                    event.tags.add(t)
            for u in all_users:
                rnd_number = random.randint(1, 15)
                if rnd_number % 2 == 0:
                    event.participants.add(u)
            event.save()
        self.stdout.write(self.style.SUCCESS(f"{number} events created!"))
