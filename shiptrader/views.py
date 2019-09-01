from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from shiptrader.models import Starship, Listing
from shiptrader.serializers import StarshipSerializer, ListingSerializer


class StarshipAPI(CreateAPIView, ListAPIView):
    serializer_class = StarshipSerializer

    def get_queryset(self):
        starship_class = self.request.query_params.get('starship_class', None)
        if starship_class is not None:
            queryset = Starship.objects.filter(
                starship_class__iexact=starship_class
            )
        else:
            queryset = Starship.objects.all()
        return queryset


class StarshipDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer


class ListingAPI(CreateAPIView, ListAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('price', 'created_at',)


class ListingDetailAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
