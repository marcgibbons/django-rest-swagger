# coding=utf-8
"""API Views for example application."""
from rest_framework.views import Response, APIView
from rest_framework import viewsets, status
from rest_framework.decorators import action, link, api_view
from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework_swagger.decorators import serializer_class

from cigar_example.app.models import Cigar, Manufacturer, Country
from .serializers import CigarSerializer, ManufacturerSerializer, \
    CountrySerializer, JambalayaSerializer


class CigarViewSet(viewsets.ModelViewSet):

    """ Cigar resource. """

    serializer_class = CigarSerializer
    model = Cigar

    def list(self, request, *args, **kwargs):
        """
        Return a list of objects.

        """
        return super(CigarViewSet, self).list(request, *args, **kwargs)

    @action()
    def set_price(self, request, pk):
        """An example action to on the ViewSet."""
        return Response('20$')

    @link()
    def get_price(self, request, pk):
        """Return the price of a cigar."""
        return Response('20$')


class ManufacturerList(ListCreateAPIView):

    """Get the list of cigar manufacturers from the database."""

    model = Manufacturer
    serializer_class = ManufacturerSerializer


class ManufacturerDetails(RetrieveUpdateDestroyAPIView):

    """Return the details on a manufacturer."""

    model = Manufacturer
    serializer_class = ManufacturerSerializer


class CountryList(ListCreateAPIView):

    """Gets a list of countries. Allows the creation of a new country."""

    model = Country
    serializer_class = CountrySerializer


class CountryDetails(RetrieveUpdateDestroyAPIView):

    """Detailed view of the country."""

    model = Country
    serializer_class = CountrySerializer

    def get_serializer_class(self):
        self.serializer_class.context = {'request': self.request}
        return self.serializer_class


class MyCustomView(APIView):

    """
    This is a custom view that can be anything at all.

    It's not using a serializer class, but I can define my own parameters.

    Cet exemple démontre l'utilisation de caractères unicode

    """

    def get(self, *args, **kwargs):
        """
        Get the single object.

        param1 -- my param

        """
        return Response({'foo': 'bar'})

    def post(self, request, *args, **kwargs):
        """
        Post to see your horse's name.

        horse -- the name of your horse

        """
        return Response({'horse': request.GET.get('horse')})


@api_view(['POST', 'GET'])
def jambalaya(request):
    """
    This is Sisko's jambalaya
    ---
    serializer: JambalayaSerializer
    """
    serializer = JambalayaSerializer(data=request.DATA)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@serializer_class(JambalayaSerializer)
@api_view(['POST'])
def jambalaya2(request):
    """
    This is Sisko's jambalaya
    """
    serializer = JambalayaSerializer(data=request.DATA)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
