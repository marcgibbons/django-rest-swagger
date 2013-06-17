from rest_framework.views import APIView


class APIDocView(APIView):

    def initial(self, request, *args, **kwargs):
        protocol = "https" if request.is_secure() else "http"
        self.host = request.build_absolute_uri()
        self.api_path = '/api'
        self.api_full_uri = "%s://%s" % (protocol, request.get_host())

        return super(APIDocView, self).initial(request, *args, **kwargs)
