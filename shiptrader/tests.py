from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shiptrader.models import Starship, Listing
from shiptrader.serializers import StarshipSerializer, ListingSerializer


class TestShiptraderAPI(APITestCase):
    def setUp(self):
        self.starship_no_1_data = {
            'cargo_capacity': 1500,
            'crew': 15,
            'hyperdrive_rating': 30.65,
            'length': 5,
            'manufacturer': 'Manufacturer 1',
            'passengers': 50,
            'starship_class': 'First Class'
        }
        self.starship_no_2_data = {
            'cargo_capacity': 3000,
            'crew': 10,
            'hyperdrive_rating': 25.50,
            'length': 9,
            'manufacturer': 'Manufacturer 2',
            'passengers': 55,
            'starship_class': 'Second Class'
        }

        self.starship_no_1_object = Starship.objects.create(**{
            'cargo_capacity': 150,
            'crew': 15,
            'hyperdrive_rating': 30.65,
            'length': 5,
            'manufacturer': 'Manufacturer 1',
            'passengers': 50,
            'starship_class': 'First Class'
        })

        self.starship_no_2_object = Starship.objects.create(**{
            'cargo_capacity': 300,
            'crew': 10,
            'hyperdrive_rating': 25.50,
            'length': 9,
            'manufacturer': 'Manufacturer 2',
            'passengers': 55,
            'starship_class': 'Second Class'
        })

        self.listing_no_1_data = {
            'name': 'Listing 1',
            'ship_type': self.starship_no_1_object.id,
            'price': 10
        }
        self.listing_no_2_data = {
            'name': 'Listing 2',
            'ship_type': self.starship_no_2_object.id,
            'price': 20
        }

        self.listing_no_1_object = Listing.objects.create(**{
            'name': 'Listing 1 object',
            'ship_type': self.starship_no_1_object,
            'price': 10
        })
        self.listing_no_2_data = Listing.objects.create(**{
            'name': 'Listing 2 object',
            'ship_type': self.starship_no_2_object,
            'price': 20
        })

    def tearDown(self):
        Starship.objects.all().delete()
        Listing.objects.all().delete(
        )

    def test_get_all_starships(self):
        url = reverse('shiptrader:starships')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_starship(self):
        url = reverse('shiptrader:starships')
        data = self.starship_no_1_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Starship.objects.count(), 3)

        new_starship = Starship.objects.filter(**self.starship_no_1_data).exists()
        self.assertTrue(new_starship)

    def test_get_starship_by_id(self):
        url = reverse('shiptrader:starship', kwargs={'pk': self.starship_no_1_object.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = StarshipSerializer(Starship.objects.get(id=self.starship_no_1_object.id))
        self.assertEqual(response.data, serializer.data)

    def test_get_not_existing_starship(self):
        url = reverse('shiptrader:starship', kwargs={'pk': 1234549})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_filter_starships_by_class(self):
        url = reverse('shiptrader:starships') + '?starship_class=First Class'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_starships_by_nonexisting_class(self):
        url = reverse('shiptrader:starships') + '?starship_class=Third Class'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_all_listings(self):
        url = reverse('shiptrader:listings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_listing(self):
        url = reverse('shiptrader:listings')
        data = self.listing_no_1_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Listing.objects.count(), 3)

        new_listing = Listing.objects.filter(**self.listing_no_1_data).exists()
        self.assertTrue(new_listing)

    def test_cant_create_listing_with_no_price(self):
        url = reverse('shiptrader:listings')
        data = self.listing_no_1_data
        data.pop('price')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_create_listing_with_no_name(self):
        url = reverse('shiptrader:listings')
        data = self.listing_no_1_data
        data.pop('name')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_listing_by_id(self):
        url = reverse('shiptrader:listing', kwargs={'pk': self.listing_no_1_object.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = ListingSerializer(Listing.objects.get(id=self.listing_no_1_object.id))
        self.assertEqual(response.data, serializer.data)

    def test_get_all_listings_sorted_by_price_ascending(self):
        url = reverse('shiptrader:listings') + '?ordering=price'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(response.data[0]['price'] < response.data[1]['price'])

    def test_get_all_listings_sorted_by_price_descending(self):
        url = reverse('shiptrader:listings') + '?ordering=-price'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(response.data[0]['price'] > response.data[1]['price'])

    def test_get_all_listings_sorted_by_time_ascending(self):
        url = reverse('shiptrader:listings') + '?ordering=created_at'
        response = self.client.get(url)

        self.assertTrue(response.data[0]['created_at'] < response.data[1]['created_at'])

    def test_get_all_listings_sorted_by_time_descending(self):
        url = reverse('shiptrader:listings') + '?ordering=-created_at'
        response = self.client.get(url)

        self.assertTrue(response.data[0]['created_at'] > response.data[1]['created_at'])

    def test_change_active_state_of_listing(self):
        url = reverse('shiptrader:listing', kwargs={'pk': self.listing_no_1_object.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['active'], True)

        response = self.client.patch(url, data={'active': False})
        self.assertEquals(response.data['active'], False)

        response = self.client.patch(url, data={'active': True})
        self.assertEquals(response.data['active'], True)
