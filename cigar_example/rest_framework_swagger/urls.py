from django.conf.urls import patterns, include
from views import SwaggerResourcesView, SwaggerApiView


urlpatterns = patterns('',
    (r'^$', SwaggerResourcesView.as_view()),
    (r'^(?P<path>\w+)/$', SwaggerApiView.as_view()),
)
