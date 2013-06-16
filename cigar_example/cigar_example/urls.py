from django.conf.urls import patterns, include

urlpatterns = patterns('',
    (r'^api/', include('cigar_example.restapi.urls', namespace="YO")),
    (r'', include('cigar_example.app.urls')),
    (r'^api/api-docs/', include('rest_framework_swagger.urls', namespace='swagger'))
)
