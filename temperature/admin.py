from django.contrib import admin

from .models import TemperatureSensor
from .models import TemperatureSample

admin.site.register(TemperatureSensor)
admin.site.register(TemperatureSample)