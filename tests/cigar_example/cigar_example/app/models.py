from django.db import models


class Cigar(models.Model):
    FORM_CHOICES = (
        ('parejo', 'Parejo'),
        ('torpedo', 'Torpedo'),
        ('pyramid', 'Pyramid'),
        ('perfecto', 'Perfecto'),
        ('presidente', 'Presidente'),
    )
    name = models.CharField(max_length=25, help_text='Cigar Name')
    colour = models.CharField(max_length=30, default="Brown")
    form = models.CharField(max_length=20, choices=FORM_CHOICES, default='parejo')
    gauge = models.IntegerField()
    length = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    notes = models.TextField()
    manufacturer = models.ForeignKey('Manufacturer')

    def get_absolute_url(self):
        return "/api/cigars/%i/" % self.id


class Manufacturer(models.Model):
    name = models.CharField(max_length=25, help_text='name of company')
    country = models.ForeignKey('Country')

    def __unicode__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=25, null=False, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class Jambalaya(models.Model):
    recipe = models.CharField(max_length=256, null=False, blank=False)
