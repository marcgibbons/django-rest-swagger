from django.contrib import admin
from .models import Cigar, Country, Manufacturer


admin.site.register(Cigar)
admin.site.register(Country)
admin.site.register(Manufacturer)
