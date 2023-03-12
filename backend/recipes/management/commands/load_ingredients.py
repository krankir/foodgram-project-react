import csv

from django.core.management import BaseCommand
from recipes.models import Ingredient

ALREADY_LOADED_ERROR_MESSAGE = 'В базе уже есть данные.'


class Command(BaseCommand):
    help = 'Загрузка из csv файла ...'

    def handle(self, *args, **kwargs):
        if Ingredient.objects.exists():
            print(ALREADY_LOADED_ERROR_MESSAGE)
        try:
            with open(
                '../data/ingredients.csv',
                encoding='utf-8',
            ) as file:
                reader = csv.reader(file)
                Ingredient.objects.bulk_create(
                    Ingredient(name=data[0],
                               measurement_unit=data[1]) for data in reader)
        except ValueError:
            print('Неопределённое значение.')
        else:
            print('загрузка окончена успешно!')
