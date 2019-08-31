import requests

from django.core.management import BaseCommand

from shiptrader.models import Starship


BASE_SWAPI_URL = 'https://swapi.co/api/'


class Command(BaseCommand):


    def make_acceptable(self, value):
        '''make string convertible to numerical value'''
        acceptable_value = None if value == 'unknown' else value.replace(',', '')
        return acceptable_value

    def import_starship(self, data):
        numerical_fields = ('length', 'hyperdrive_rating', 'passengers', 'crew', 'cargo_capacity')
        text_fields = ('model', 'starship_class', 'manufacturer')

        starship_data = {}
        for field in text_fields:
            starship_data[field] = data[field]

        for field in numerical_fields:
            starship_data[field] = self.make_acceptable(data[field])

        starship = Starship.objects.create(**data)
        self.stdout.write('Imported Starship {}'.format(starship))


    def handle(self, *args, **options):

        current_endpoint = BASE_SWAPI_URL + 'starships/?page=1'

        while current_endpoint:
            self.stdout.write('Current page {}'.format(current_endpoint))
            results = requests.get(current_endpoint).json()
            for starship_data in results:
                self.import_starship(starship_data)
            current_endpoint = results['next']
