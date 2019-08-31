from django.conf.urls import url

from shiptrader import views


urlpatterns = [
    url(r'^starships/$', views.StarshipAPI.as_view(), name='get_starships'),
    url(r'^starships/(?P<pk>[0-9]+)/$', views.StarshipDetailAPI.as_view(), name='get_starship'),

    url(r'^listings/$', views.ListingAPI.as_view(), name='get_listings'),
    url(r'^listings/(?P<pk>[0-9]+)/$', views.ListingDetailAPI.as_view(), name='get_listing'),
]