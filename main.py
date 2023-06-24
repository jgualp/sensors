#!/usr/bin/env python
from django.core.wsgi import get_wsgi_application
import os

# Establim l'arxiu settings.py que utilitzarem (el que està dins de sensors/).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sensors.settings")

# Instanciem un web service WSGI per tenir-lo com a passarel·la per al nostre django.
application = get_wsgi_application()

from temperature.models import TemperatureSensor, TemperatureSample
import glob
from datetime import datetime, timedelta
import time

# Carreguem els drivers del sensor de temperatura.
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Configurem l'accés a les lectures del sensor. Això té a veure amb 
# el funcionament del sensor Dallas DS18B20.
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Aquestes dues funcions implementen la lectura de mostres de temperatura
# del sensor que tenim connectat al RPI.
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# Cada cop que executem aquest programa, agafem una mostra de la temperatura del
# sensor i la guardem a la BD a través del model de dades de l'aplicació.
ts = datetime.now() + timedelta(hours=2)
mostra = TemperatureSample(sensor_id=1, value=read_temp(), timestamp=ts)
mostra.save()
