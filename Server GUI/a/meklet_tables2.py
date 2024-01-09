from a import tables as t
from a import models as m
from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin


class FilteredPersonListView(SingleTableMixin, FilterView):
    table_class = t.SensorTable
    model = m.SensorMeta
    template_name = "meklet_tables2_list.html"

    filterset_class = t.SensorFilter


def sensor_list(request):
    table = t.SensorTable(m.SensorMeta.objects.all())

    return render(request, "meklet_tables2_list.html", {
        "table": table
    })
