import django_tables2 as t
from a import models as m

class SensorTable(t.Table):
    modcol = t.TemplateColumn("{{record.hub.model}}# {{record.hub.nr}}",
                              verbose_name="Attached to:")

    #hub_att = t.LinkColumn('sample-detail', args=[t.A('model')])
    class Meta:
        model = m.SensorMeta
        #hub = t.ManyToManyColumn(transform=lambda hub: hub.transform(f"{hub.model} #{hub.nr}"))
        #fields = ("nr", "model",  "hub_att", "loc_ro", "comment", ) 
        #hub = t.ManyToManyColumn(transform=lambda hub:f"{hub.model} #{hub.nr}")
        sequence = ("nr", "model", "modcol", "loc_ro", "comment", )
        exclude = ( "interface", "hub")
