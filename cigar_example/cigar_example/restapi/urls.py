from django.conf.urls import patterns, include, url

from cigar_example.restapi import views as api_views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^custom$', api_views.MyCustomView.as_view()),
     url(r'^cigars/?$', api_views.CigarList.as_view(), name='list_of_cigars'),
     url(r'^cigars/(?P<pk>\d+)/?$', api_views.CigarDetails.as_view(), name='cigar_details'),

     url(r'^manufacturers/?$', api_views.ManufacturerList.as_view(), name='list_of_manufacturers'),
     url(r'^manufacturers/(?P<pk>\d+)/?$', api_views.ManufacturerDetails.as_view(), name='manufacturer_details'),

     url(r'^countries/?$', api_views.CountryList.as_view(), name='list_of_countries'),
     url(r'^countries/(?P<pk>\d+)/?$', api_views.CountryDetails.as_view(), name='countries_details'),

)
