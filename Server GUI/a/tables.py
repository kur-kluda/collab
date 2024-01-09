import django_tables2 as t
from a import models as m

class SensorTable(t.Table):

    #render_foo methods are only called if the value for a cell is 
    #determined to be not an empty value.
    # When a value is in Column.empty_values, a default value is rendered 
    #instead (both Column.render and Table.render_FOO are skipped).

    #modcol = t.ManyToManyColumn(accessor="hub__model",
    #modcol = t.TemplateColumn("{{model}}# {{nr}}",
    #modcol = t.TemplateColumn("{{hub__model}}# {{hub__nr}}",
        #accessor="hub__model",
        # nevar šādi, nevar tādi...
        #accessor="hub__model+hub__nr",
                                #'HubMeta' object has no attribute 'exists'
                      #transform = lambda h: "teeeeeeee",
    #    verbose_name="Attached to:",
    #                   empty_values=(),
                          
    #)#transform=lambda r: f"{r.hub.model} #{r.hub.nr}")
    modcol = t.TemplateColumn("{{record.hub.model}}# {{record.hub.nr}}")

    #hub_att = t.LinkColumn('sample-detail', args=[t.A('model')])
    class Meta:
        model = m.SensorMeta
        fields = ("hub", "modcol", "ert", "hub__model")
        # "hub",
        #hub = t.ManyToManyColumn(transform=lambda hub: hub.transform(f"{hub.model} #{hub.nr}"))
        #fields = ("nr", "model",  "hub_att", "loc_ro", "comment", ) 
        #sequence = ("nr", "model", "hub_namenr", "loc_ro", "comment", )
        #hub = t.ManyToManyColumn(transform=lambda hub:f"{hub.model} #{hub.nr}")
        #sequence = ("nr", "model", "hub", "loc_ro", "comment", )
        #exclude = ( "interface", )
    #def render_modcol(self):
    #    print("rrhhhhhhr")
    #    return True
    #    return "GOOOOONE"
    #    return f"{r.model} #{r.nr}"
    #
    #def render_modcol(self, val):
    #    print("rrhhhhhhr")
    #    return True
    #    return "GOOOOONE"
    #    return f"{r.model} #{r.nr}"
#
    #def render_modcol(self, val, r):
    #    print("rrhhhhhhr")
    #    return True
    #    return "GOOOOONE"
    #    return f"{r.model} #{r.nr}"

    def render_hub_namenr(self, val, r):
        return "GOOOOONE"
        h = r.hub
        if h:
            return f"{h.model} #{h.nr}" if h.model and h.nr else 'N/A'
        return 'N/AA'
        print("rrr")
        return f"{r.hub.model} #{r.hub.nr}"
