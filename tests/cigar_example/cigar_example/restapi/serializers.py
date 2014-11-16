from rest_framework import serializers
from rest_framework import fields
from cigar_example.app import models


class CigarSerializer(serializers.ModelSerializer):
    url = fields.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = models.Cigar


class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Manufacturer


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Country


class JambalayaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Jambalaya


class JambalayaQuerySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, required=False)
    origin = serializers.CharField(max_length=20, required=False)


class CigarJambalayaSerializer(serializers.Serializer):
    cigar = CigarSerializer()
    jambalaya = JambalayaSerializer()
