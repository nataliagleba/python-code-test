import requests
import traceback

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
        text_fields = ('starship_class', 'manufacturer')

        starship_data = {}
        for field in text_fields:
            starship_data[field] = data[field]

        for field in numerical_fields:
            starship_data[field] = self.make_acceptable(data[field])

        starship = Starship.objects.create(**starship_data)
        self.stdout.write('Imported Starship ID: {}'.format(starship.id))


    def handle(self, *args, **options):

        current_endpoint = BASE_SWAPI_URL + 'starships/?page=1'

        failed, succed = 0, 0
        while current_endpoint:
            self.stdout.write('Current page {}'.format(current_endpoint))
            results = requests.get(current_endpoint).json()
            for starship_data in results['results']:
                try:
                    self.import_starship(starship_data)
                    succed += 1
                except Exception as e:
                    failed += 1
                    traceback.print_exc()
            current_endpoint = results['next']
        self.stdout.write('Finished. \n Succesfully imported {} starship. \n {} starships failed to import'.format(succed, failed))
