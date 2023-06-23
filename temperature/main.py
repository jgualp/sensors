# Instatiate Django and import settings
import os
import glob
import time

#mark django settings module as settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sensors.settings")

#instantiate a web sv for django which is a wsgi
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

#import your models schema
from temperature.models import TemperatureSensor

#Create Operations here
# manuf_model = models.CharField(max_length=128)
#    location_desc = models.CharField(max_length=128)
#    location_geo_lat = models.FloatField()
#    location_geo_lng = models.FloatField()

sensor = TemperatureSensor(manuf_model="Dallas DS18B20", location_desc="Home", location_geo_lat=0, location_geo_lng=0)
sensor.save()

# Read operation logic
#person = Person.objects.get()

#print(f'Hello, I am {person.name}, {person.age} y/o. Reachable at {person.email}')
#Prints Hello, I am Nimish, 23 y/o. Reachable at nimishverma@ymail.com