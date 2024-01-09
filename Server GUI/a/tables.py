import django_tables2 as t
from a import models as m

from django_filters import FilterSet
#from .models import SensorMeta

class SensorFilter(FilterSet):
    class Meta:
        model = m.SensorMeta
        fields = {"model": ["contains"], "hub__model": ["contains"], "interface__interface": ["contains"], "loc_ro": ["exact"], "comment": ["contains"]}

class SensorTable(t.Table):
    modcol = t.TemplateColumn("{{record.hub.model}}# {{record.hub.nr}}",
                              verbose_name="Attached to:")
    #KeyError if in sequence but not fields explicit..
    infacecol = t.TemplateColumn("{{record.interface.interface}}",
                              verbose_name="Attached via:")

    #hub_att = t.LinkColumn('sample-detail', args=[t.A('model')])
    class Meta:
        model = m.SensorMeta
        #hub = t.ManyToManyColumn(transform=lambda hub: hub.transform(f"{hub.model} #{hub.nr}"))
        #fields = ("nr", "model",  "hub_att", "loc_ro", "comment", ) 
        #hub = t.ManyToManyColumn(transform=lambda hub:f"{hub.model} #{hub.nr}")
        sequence = ("nr", "model", "modcol", "infacecol", "loc_ro", "comment", )
        exclude = ( "hub", "interface")
