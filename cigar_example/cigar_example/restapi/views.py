from rest_framework.views import Response, APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from cigar_example.app.models import Cigar, Manufacturer, Countries
from serializers import CigarSerializer, ManufacturerSerializer, CountrySerializer


class CigarList(ListCreateAPIView):
    """
    Lists and creates cigars from the database.
    """

    model = Cigar
    """ This is the model """
    serializer_class = CigarSerializer


class CigarDetails(RetrieveUpdateDestroyAPIView):
    """
    Detailed view of an individual cigar record.

    Can be updated and deleted. Each cigar must
    be assigned to a manufacturer
    """
    model = Cigar
    serializer_class = CigarSerializer


class ManufacturerList(ListCreateAPIView):
    """
    Gets the list of cigar manufacturers from the database.
    """
    model = Manufacturer
    serializer_class = ManufacturerSerializer

class ManufacturerDetails(RetrieveUpdateDestroyAPIView):
    """
    Returns the details on a manufacturer
    """
    model = Manufacturer
    serializer_class = ManufacturerSerializer

class CountryList(ListCreateAPIView):
    """
    Gets a list of countries. Allows the creation of a new country.
    """
    model = Countries
    serializer_class = CountrySerializer

class CountryDetails(RetrieveUpdateDestroyAPIView):
    """
    Detailed view of the country
    """
    model = Countries
    serializer_class = CountrySerializer

class MyCustomView(APIView):
    """
    This is a custom view that can be anything at all. It's not using a serializer class,
    but I can define my own parameters like so!

    This is a new line

    horse -- the name of your horse

    """
    def get(self, *args, **kwargs):
        """ Docs there """
        return Response({'foo':'bar'})
    def post(self, request, *args, **kwargs):
        return Response({'horse': request.GET.get('horse')})
