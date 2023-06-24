import locale
from django.db import models

# Definició de la classe que representarà els sensors que tinguem, permetent registrar
# el fabricant i model de sensor, una descripció de la seva ubicació i les coordenades
# geogràfiques de la seva ubicació.
class TemperatureSensor(models.Model):
    manuf_model = models.CharField(max_length=128)
    location_desc = models.CharField(max_length=128)
    location_geo_lat = models.FloatField()
    location_geo_lng = models.FloatField()

    def __str__(self):
        return self.location_desc + " (" + self.manuf_model + ")"

# Definició de la classe que representarà les mesures obtingudes pels sensors. Permet
# registrar el valor de la mesura, la data/hora en què ha estat presa i, també, permet
# mantenir l'associació amb el sensor amb el qual ha estat obtinguda.
class TemperatureSample(models.Model):
    sensor = models.ForeignKey(TemperatureSensor, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField("Date/time observed")

    def __str__(self):
        locale.setlocale(locale.LC_ALL, '')
        valor = locale.format('%.2f', self.value)
        return self.sensor.location_desc + " - " + valor + "ºC - " + self.timestamp.strftime("%Y/%m/%d %H:%M:%S")

