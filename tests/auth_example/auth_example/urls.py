from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include('auth_example.restapi.urls', namespace="cigars")),
    (r'^', include('rest_framework_swagger.urls', namespace='swagger'))
)
