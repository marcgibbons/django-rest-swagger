from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter

from auth_example.restapi import views as views


router = DefaultRouter()
router.register(r'cigars', views.CigarViewSet)

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^custom$', views.MyCustomView.as_view()),
    url(r'^manufacturers/?$', views.ManufacturerList.as_view(), name='list_of_manufacturers'),
    url(r'^manufacturers/(?P<pk>\d+)/?$', views.ManufacturerDetails.as_view(), name='manufacturer_details'),

    url(r'^countries/?$', views.CountryList.as_view(), name='list_of_countries'),
    url(r'^countries/(?P<pk>\d+)/?$', views.CountryDetails.as_view(), name='countries_details'),
)

urlpatterns += router.urls
