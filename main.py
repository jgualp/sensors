#!/usr/bin/env python

import os
from django.core.wsgi import get_wsgi_application
from temperature.models import TemperatureSensor

# Establim l'arxiu settings.py que utilitzarem (el que està dins de sensors/).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sensors.settings")

# Instanciem un web service WSGI per tenir-lo com a passarel·la per al nostre django.
application = get_wsgi_application()

# Provem algunes operacions de persistència d'objectes amb les classes que tenim definides al nostre model.
sensor = TemperatureSensor(manuf_model="Dallas DS18B20", location_desc="Home", location_geo_lat=0, location_geo_lng=0)
sensor.save()

# Read operation logic
#person = Person.objects.get()

#print(f'Hello, I am {person.name}, {person.age} y/o. Reachable at {person.email}')
#Prints Hello, I am Nimish, 23 y/o. Reachable at nimishverma@ymail.com