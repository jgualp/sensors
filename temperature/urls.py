from django.urls import path

from . import views

app_name = "temperature"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:sensor_id>/graph_form/", views.graph_form, name="graph_form"),
    path("<int:sensor_id>/graph_view/", views.graph_view, name="graph_view"),
]