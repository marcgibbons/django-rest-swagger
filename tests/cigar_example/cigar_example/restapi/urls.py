from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter

from cigar_example.restapi import views as views


router = DefaultRouter()
router.register(r'cigars', views.CigarViewSet)
router.register(r'artisan_cigars', views.ArtisanCigarViewSet)

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^custom$', views.MyCustomView.as_view()),
    url(r'^manufacturers/?$', views.ManufacturerList.as_view(), name='list_of_manufacturers'),
    url(r'^manufacturers/(?P<pk>\d+)/?$', views.ManufacturerDetails.as_view(), name='manufacturer_details'),

    url(r'^countries/?$', views.CountryList.as_view(), name='list_of_countries'),
    url(r'^countries/(?P<pk>\d+)/?$', views.CountryDetails.as_view(), name='countries_details'),
    url(r'^jambalaya_create/$', views.create_jambalaya, name='create-jambalaya'),
    url(r'^jambalaya_find/$', views.find_jambalaya, name='find-jambalaya'),
    url(r'^jambalaya_retrieve/$', views.retrieve_jambalaya, name='retrieve-jambalaya'),
    url(r'^drop_cigar_in_jambalaya/$', views.drop_cigar_in_jambalaya, name='cigar-jambalaya'),
)

urlpatterns += router.urls
