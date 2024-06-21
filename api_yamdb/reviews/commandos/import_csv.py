import csv
import os

from django.core.management import BaseCommand
from django.db import IntegrityError

from api_yamdb.settings import BASE_DIR
from reviews.models import (
    Categorie,
    Comment,
    Genre,
    Review,
    Title,
    User
)


ThroughModel = Title.genre.through

FILES_CLASSES = {
    'category': Categorie,
    'genre': Genre,
    'titles': Title,
    'genre_title': ThroughModel,
    'users': User,
    'review': Review,
    'comments': Comment,
}

KEY_FIELDS = {
    'category': ('category', Categorie),
    'title_id': ('title', Title),
    'genre_id': ('genre', Genre),
    'author': ('author', User),
    'review_id': ('review', Review),
}

local_csv_dir = os.path.join(BASE_DIR, 'static\\data\\')


def open_csv(file_name):
    csv_path = os.path.join(local_csv_dir, file_name + '.csv')
    try:
        with (open(csv_path, encoding='utf-8')) as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        print(f'Файл {file_name}.csv не найден.')
        return


def change_fk_values(data_csv):
    data_csv_copy = data_csv.copy()
    for field_key, field_value in data_csv.items():
        if field_key in KEY_FIELDS.keys():
            field_key0 = KEY_FIELDS[field_key][0]
            data_csv_copy[field_key0] = KEY_FIELDS[field_key][1].objects.get(
                pk=field_value)
    return data_csv_copy


def import_csv(file_name, class_name):
    data = open_csv(file_name)
    rows = data[1:]
    for row in rows:
        data_csv = dict(zip(data[0], row))
        data_csv = change_fk_values(data_csv)
        try:
            table = class_name(**data_csv)
            table.save()
        except (ValueError, IntegrityError) as error:
            print(f'Ошибка в загружаемых данных. {error}. '
                  f'Таблица {class_name.__qualname__} не загружена.')
            break
    print(f'Таблица {class_name.__qualname__} импортирована.')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for key, value in FILES_CLASSES.items():
            print(f'Импортирование таблицы {value.__qualname__}')
            import_csv(key, value)
