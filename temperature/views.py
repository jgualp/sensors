from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .models import TemperatureSample, TemperatureSensor
from .fusioncharts import FusionCharts, FusionTable, TimeSeries
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


# Vista formulari per configurar la gràfica que volem visualitzar (escollir data).
class GraphForm(forms.Form):
    data = forms.DateField(label="Data")

def graph_form(request, sensor_id):
    gf = GraphForm()
    return render(request, "temperature/graph_form.html", {"form": gf, "id":sensor_id})

# Vista de la gràfica que recull la data del formulari i genera la gràfica d'aquell dia.
def graph_view(request, sensor_id):
    if request.method=="POST":

        form = GraphForm(request.POST)

        if form.is_valid():
            # Preparem les dades i configuracions generals de la gràfica.
            sensor = get_object_or_404(TemperatureSensor, pk=sensor_id)
            data = form.cleaned_data["data"]
    
            start = str(data) + ' 00:00:00.000000'
            end = str(data) + ' 23:59:59.999999'

            # Codi anul·lat, era una primera versió amb un model bàsic de gràfica que
            # no dóna proporcionalitat temporal.
            """
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
            """
            
            # Preparem l'schema i les dades per a una gràfica de tipus "timeseries": és
            # una gràfica de línia, amb proporcionalitat temporal.
            schema = [{
                "name": "Hora",
                "type": "date",
                "format": "%d-%m-%Y %H:%M:%S"
            }, {
                "name": "Temperatura (ºC)",
                "type": "number"
            }]
            dades_temp = []

            # Les dades, les afegim consultant-les de la BD.
            for key in TemperatureSample.objects.filter(timestamp__range=(start, end)).filter(sensor__id=sensor_id):
                mostra = []
                mostra.append(key.timestamp.strftime('%d-%m-%Y %H:%M:%S'))
                mostra.append(float(key.value))
                dades_temp.append(mostra)

            # Creem els objectes que necessita el constructor de la gràfica.
            fusionTable = FusionTable(schema, dades_temp)
            timeSeries = TimeSeries(fusionTable)
            

            # Creem un objecte per a la gràfica utilitzant el constructor de FusionCharts: "line"
            # El cinquè paràmetre, ha de coincidir amb el nom del <div> de la template HTML on
            # volem que es visualitzi la gràfica.
            grafica = FusionCharts("timeseries", "ex1" , "1200", "600", "viewtemp", "json", timeSeries)
            
            # "outuput" és el nom de la variable de substitució que tenim a la template HTML.
            return render(request, 'temperature/graph_view.html', {'output': grafica.render()})
            
        

    return HttpResponseRedirect(reverse("temperature:graph_form"))
