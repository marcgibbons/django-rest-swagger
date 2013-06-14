from rest_framework.views import APIView


class APIDocView(APIView):

    def initial(self, request, *args, **kwargs):
        self.host = request.build_absolute_uri()

        return super(APIDocView, self).initial(request, *args, **kwargs)
