class DbRouter:
    meta_db = "meta-db"
    default_db = "default"
    business_entities = ["HubMeta",
                         "SensorMeta"]

    def db_for_read(self, model, **hints):
        model_name = model._meta.model_name
       # print(f"mnme: {model_name}")
        if model_name in self.business_entities:
            return self.meta_db
        else:
            return self.default_db

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, hints)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
       # print(f"apppl: {app_label}, mdl: {str(model_name)}")
        if app_label in self.business_entities or app_label in ['a', 'g']:
            return db == self.meta_db
        else:
            return db == self.default_db