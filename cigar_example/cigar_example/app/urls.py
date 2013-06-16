from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'/', include('rest_framework_docs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
