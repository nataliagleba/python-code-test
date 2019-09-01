from rest_framework import serializers

from shiptrader.models import Listing, Starship


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
        extra_kwargs = {
            'price': {'required': True},
            'name': {'required': True}
        }


class StarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Starship
        fields = '__all__'
