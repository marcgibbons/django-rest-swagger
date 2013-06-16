from django.conf.urls import patterns, include

urlpatterns = patterns('',
    (r'^api/', include('cigar_example.restapi.urls', namespace="cigars")),
    (r'^', include('rest_framework_swagger.urls', namespace='swagger'))
)
