# coding=utf-8
"""API Views for example application."""
from rest_framework.views import Response, APIView
from rest_framework import viewsets, status
import rest_framework

from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView

from cigar_example.app.models import Cigar, Manufacturer, Country, Jambalaya
from .serializers import CigarSerializer, ManufacturerSerializer, \
    CountrySerializer, JambalayaSerializer, JambalayaQuerySerializer, \
    CigarJambalayaSerializer, JambalayaCigarsSerializer, CigarSerializerMinimal

if rest_framework.VERSION < '3.0.0':
    from rest_framework.decorators import action, link, api_view
else:
    from rest_framework.decorators import detail_route, api_view

    def action():
        return lambda func: detail_route(methods=['post'])(func)

    def link():
        return lambda func: detail_route()(func)


class CigarViewSet(viewsets.ModelViewSet):

    """ Cigar resource. """

    serializer_class = CigarSerializer
    model = Cigar
    queryset = Cigar.objects.all()

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


class ArtisanCigarViewSet(viewsets.ModelViewSet):

    """
    Cigar resource.
    ---
    get_price:
        omit_serializer: true
    set_price:
        omit_serializer: true
        parameters_strategy:
            form: replace
        parameters:
            - name: price
              type: number
    """

    serializer_class = CigarSerializer
    model = Cigar
    queryset = Cigar.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Return a list of objects.

        """
        return super(ArtisanCigarViewSet, self).list(request, *args, **kwargs)

    @action()
    def set_price(self, request, pk):
        """An example action to on the ViewSet."""
        return Response('20$')

    @link()
    def get_price(self, request, pk):
        """Return the price of a cigar."""
        return Response('20$')


class ManufacturerList(ListCreateAPIView):
    """
    Get the list of cigar manufacturers from the database.

    Excludes artisan manufacturers.
    """

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


@api_view(['POST'])
def find_jambalaya(request):
    """
    Retrieve a *jambalaya* recipe by name or country of origin
    ---
    request_serializer: JambalayaQuerySerializer
    response_serializer: JambalayaSerializer
    """
    if request.method == 'POST':
        serializer = JambalayaQuerySerializer(data=request.DATA)
        if serializer.data['name'] is not None:
            j = Jambalaya.objects.filter(recipe__contains='name=%s' % serializer.data['name'])
        else:
            j = Jambalaya.objects.filter(recipe__contains="country=%s" % serializer.data['origin'])
        serializer = JambalayaSerializer(j, many=True)
        return Response(serializer.data)
    else:
        return Response("", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def retrieve_jambalaya(request):
    """
    Retrieve a jambalaya recipe by name or country of origin
    ---
    serializer: JambalayaSerializer
    parameters:
        - name: name
          description: name as found in recipe
          type: string
          paramType: query
          required: false
        - name: origin
          type: string
          paramType: query
          required: false
    """
    if request.method == 'GET':
        serializer = JambalayaQuerySerializer(data=request.DATA)
        if serializer.data['name'] is not None:
            j = Jambalaya.objects.filter(recipe__contains='name=%s' % serializer.data['name'])
        else:
            j = Jambalaya.objects.filter(recipe__contains="country=%s" % serializer.data['origin'])
        serializer = JambalayaSerializer(j, many=True)
        return Response(serializer.data)
    else:
        return Response("", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_jambalaya(request):
    """
    Create a jambalaya recipe
    ---
    serializer: JambalayaSerializer
    """
    serializer = JambalayaSerializer(data=request.DATA)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def drop_cigar_in_jambalaya(request):
    """
    Make a cigar jambalaya
    ---
    serializer: ..serializers.CigarJambalayaSerializer
    """
    serializer = CigarJambalayaSerializer(data=request.DATA)
    if serializer.is_valid():
        return Response("mmm.. an acquired taste!", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def mix_cigars_in_jambalaya(request):
    """
    Make a diverse cigar jambalaya. (In case you're wondering, I have no idea
    how to try out this api, it just illustrates what nested many=True
    serializers look like in swagger)
    ---
    serializer: ..serializers.JambalayaCigarsSerializer
    """
    serializer = JambalayaCigarsSerializer(data=request.DATA)
    if serializer.is_valid():
        return Response("mmm.. an acquired taste!",
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_cigar2(request):
    """
    ---
    response_serializer: CigarSerializer
    parameters:
        - name: body
          pytype: CigarSerializerMinimal
          paramType: body
    """
    in_serializer = CigarSerializerMinimal(data=request.DATA)
    if in_serializer.is_valid():
        cigar = Cigar()
        cigar.name = in_serializer.data['name']
        cigar.gauge = in_serializer.data['gauge']
        cigar.length = 2
        cigar.price = 2
        manufacturer = Manufacturer.objects.first()
        if manufacturer is None:
            manufacturer = Manufacturer()
            manufacturer.name = 'Taco tobacco'
            country = Country.objects.first()
            if country is None:
                country = Country()
                country.name = "Watchacallistan"
                country.save()
            manufacturer.country = country
            manufacturer.save()
        cigar.manufacturer = manufacturer
        cigar.save()
        out_serializer = CigarSerializer(cigar)
        return Response(out_serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response(in_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
