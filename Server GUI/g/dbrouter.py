class DbRouter:
    meta_db = "meta-db"
    default_db = "default"
    business_entities = ["HubMeta".lower(),
                         "SensorMeta".lower(),
                         "Connection_InterfaceMeta".lower(),
                         "MeasureMeta".lower(),
                         "sensormeta_measurements".lower()
                         ]
    
    def routeToBase(self, model_name)-> bool:
        if model_name.lower()[0]=="a" and model_name.lower()[1]=="_":
            return self.meta_db
        else: return self.default_db
#, whoishere="nothererere---",
    def db_for_read(self, model, **hints):
        #return self.routeToBase(model._meta.model_name)
        return self.routeToBase(model._meta.db_table)

    def db_for_write(self, model, **hints):
        #return self.routeToBase(model._meta.model_name)
        return self.routeToBase(model._meta.db_table)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
       # print(f"apppl: {app_label}, mdl: {str(model_name)}")
        if app_label in self.business_entities or app_label in ['a', 'g']:
            return db == self.meta_db
        else:
            return db == self.default_db