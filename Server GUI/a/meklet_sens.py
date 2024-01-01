from django.shortcuts import render

class hubmeta:
    def __init__(self):
        self.model= "NONO"
        self.sensors_ids = [1]
        self.location = [56.00002, 78.000009]

    def __init__(self, model, sensors):
        self.model= model
        self.sensors_ids = sensors        


class sensormeta:
    def __init__(s):
        s.model="DHT11" #->: str
        s.measurements= [ "t", "hum"] 
        s.ranges= [[0,90,2], [0, 90, 2]]
        s.hub_ids= [1]
        s.location= [56.00002, 78.00091]

view_resolver= {
    "": "meklet_strap.html",
    "b": "meklet_strap.html",
    "t": "meklet_table.html",
}

def search_sensors(r, renderer):
    #print(list2str(sensormeta().hub_ids))
    view_model = {
        'search_term' : '',
        'selected_sensors' :{},
        'all_sensors': [sensormeta(),
                        sensormeta(),
                        sensormeta()],
        #TODO: add paging??
        'page': 1,
        'totalpages': 100
    }
    if(view_resolver.get(renderer.strip("/"))):
        return render(r, view_resolver[renderer.strip("/")], view_model)
    else:
        return render(r, view_resolver[""], view_model)