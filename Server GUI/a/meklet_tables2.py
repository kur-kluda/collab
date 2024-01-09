from a import tables as t
from a import models as m
from django.shortcuts import render

def sensor_list(request):
    table = t.SensorTable(m.SensorMeta.objects.all()[:30])

    return render(request, "meklet_tables2_list.html", {
        "table": table
    })
