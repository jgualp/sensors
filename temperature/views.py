from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .models import TemperatureSample, TemperatureSensor
from .fusioncharts import FusionCharts
from django.template import loader
from django.urls import reverse
from datetime import datetime

# Vista inicial (root).
def index(request):
    latest_sensor_list = TemperatureSensor.objects.order_by("manuf_model")
    template = loader.get_template("temperature/index.html")
    context = {
        "latest_sensor_list": latest_sensor_list,
    }
    return HttpResponse(template.render(context, request))


# Vista formulari per configurar la gràfica que volem visualitzar.
class GraphForm(forms.Form):
    #data_hora_inicial = forms.DateTimeField(label="Data/hora inicial")
    #data_hora_final = forms.DateTimeField(label="Data/hora final")
    data = forms.DateField(label="Data")

def graph_form(request, sensor_id):
    gf = GraphForm()
    return render(request, "temperature/graph_form.html", {"form": gf, "id":sensor_id})

def graph_view(request, sensor_id):
    if request.method=="POST":

        form = GraphForm(request.POST)

        if form.is_valid():
            sensor = get_object_or_404(TemperatureSensor, pk=sensor_id)
            data = form.cleaned_data["data"]
    
            start = str(data) + ' 00:00:00.000000'
            end = str(data) + ' 23:59:59.999999'
            #user = UserAccount.objects.filter(created_at__gte=start, created_at__lte=end)
            #user = UserAccount.objects.filter(created_at__range=(start, end))


            dataSource = {}
            dataSource['chart'] = {
                "caption": "Evolució de la temperatura",
                "subCaption": str(sensor),
                "xAxisName": "Data/Hora",
                "yAxisName": "Temperatura (ºC)",
                "numberSuffix": "ºC",
                "theme": "zune",
            }

            dataSource['data'] = []

            # Iterem sobre les mostres de temperatura seleccionant les del dia seleccionat i del sensor que toca.
            for key in TemperatureSample.objects.filter(timestamp__range=(start, end)).filter(sensor__id=sensor_id):
                data = {}
                data['label'] = key.timestamp.strftime('%H:%M:%S')
                data['value'] = float(key.value)
                dataSource['data'].append(data)

            # Create an object for the Column 2D chart using the FusionCharts class constructor
            line2D = FusionCharts("line", "ex1" , "1200", "600", "viewtemp", "json", dataSource)
            return render(request, 'temperature/graph_view.html', {'output': line2D.render()})
            #return HttpResponse(dataSource['data'])
        

    return HttpResponseRedirect(reverse("temperature:graph_form"))