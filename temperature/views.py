from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .models import TemperatureSample, TemperatureSensor
from .fusioncharts import FusionCharts
from django.template import loader
from django.urls import reverse

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
    data_hora_inicial = forms.DateTimeField(label="Data/hora inicial")
    data_hora_final = forms.DateTimeField(label="Data/hora final")

def graph_form(request, sensor_id):
    gf = GraphForm()
    return render(request, "temperature/graph_form.html", {"form": gf, "id":sensor_id})

def graph_view(request, sensor_id):
    if request.method=="POST":
        sensor = get_object_or_404(TemperatureSensor, pk=sensor_id)

        dataSource = {}
        dataSource['chart'] = {
            "caption": "Evolució de la temperatura",
            "subCaption": str(sensor),
            "xAxisName": "Data/Hora",
            "yAxisName": "Temperatura (ºC)",
            "numberSuffix": "ºC",
            "theme": "fusion",
        }

        dataSource['data'] = []

        # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
        for key in TemperatureSample.objects.all():
            data = {}
            data['label'] = str(key.timestamp)
            data['value'] = float(key.value)
            dataSource['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
        line2D = FusionCharts("line", "ex1" , "600", "350", "viewtemp", "json", dataSource)
        return render(request, 'temperature/graph_view.html', {'output': line2D.render()})
        #return HttpResponse(dataSource['data'])
        

    return HttpResponseRedirect(reverse("temperature:graph_form"))