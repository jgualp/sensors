import locale
from django.db import models
from django.contrib.gis.db import models


class TemperatureSensor(models.Model):
    manuf_model = models.CharField(max_length=128)
    location_desc = models.CharField(max_length=128)
    location_geo_lat = models.FloatField()
    location_geo_lng = models.FloatField()

    def __str__(self):
        return self.location_desc + " (" + self.manuf_model + ")"


class TemperatureSample(models.Model):
    sensor = models.ForeignKey(TemperatureSensor, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField("Date/time observed")

    def __str__(self):
        locale.setlocale(locale.LC_ALL, '')
        valor = locale.format('%.2f', self.value)
        return self.sensor.location_desc + " - " + valor + "ºC - " + self.timestamp.strftime("%Y/%m/%d %H:%M:%S")
    
    def __unicode__(self):
        return u'%.2f' % self.value

