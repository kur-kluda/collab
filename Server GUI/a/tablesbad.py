"""import django_tables2 as t
from a import models as m

from django_filters import FilterSet
#from .models import SensorMeta
class SensorMixin(t.Table):
    modcol = t.TemplateColumn("{{record.hub.model}}# {{record.hub.nr}}",
                              verbose_name="Attached to:")
    




class SensorTable(SensorMixin, t.Table):
    #hub_att = t.LinkColumn('sample-detail', args=[t.A('model')])
    class Meta:
        model = m.SensorMeta
        #hub = t.ManyToManyColumn(transform=lambda hub: hub.transform(f"{hub.model} #{hub.nr}"))
        #fields = ("nr", "model",  "hub_att", "loc_ro", "comment", ) 
        #hub = t.ManyToManyColumn(transform=lambda hub:f"{hub.model} #{hub.nr}")
        sequence = ("nr", "model", "modcol", "loc_ro", "comment", )
        exclude = ( "interface", "hub")

class SensorFilter(FilterSet):
    class Meta:
        #'TableOptions' object has no attribute 'get_field'
        #model = SensorTable
        #'TableOptions' object has no attribute 'get_field'
        #model = SensorMixin
        #'TableOptions' object has no attribute 'get_field'. Did you mean: 'page_field'?
        model = m.SensorMeta
        fields = {"model": ["contains"], "modcol": ["contains"], "loc_ro": ["exact"], "comment": ["contains"]}

        """
