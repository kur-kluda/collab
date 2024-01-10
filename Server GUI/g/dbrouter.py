class DbRouter:#šā klase definē Django datu bāzes maršrutētāju, lai zinātu uz kuru datu bāzi nosūtītīt modeļa datus.
    meta_db = "meta-db"
    default_db = "default"
    business_entities = ["HubMeta".lower(),
                         "SensorMeta".lower(),
                         "Connection_InterfaceMeta".lower(),
                         "MeasureMeta".lower(),
                         "sensormeta_measurements".lower()
                         ]#business_entities satur modeļu nosaukumus, kas ir kā metadatu modeļi, kuri tiks maršrutēti uz meta_db (veicot lasīšanu/rakstīšanu)
    
    def routeToBase(self, model_name)-> bool:#metode routeToBase() izmanto modeļu nosaukumus kā ievadi, un atgriež to datubāzes nosaukumu, uz kuru modeli maršrutēs atkarībā no modeļa nosaukuma nosacījuma - sākas ar "a_.
        if model_name.lower()[0]=="a" and model_name.lower()[1]=="_":
            return self.meta_db
        else: return self.default_db
#, whoishere="nothererere---",
#metodes db_for_read() un db_for_write() izsauc metodi routeToBase(), lai noteiktu, kurā db ir jāielasa un jāieraksta modeļa dati.
    def db_for_read(self, model, **hints):
        #return self.routeToBase(model._meta.model_name)
        return self.routeToBase(model._meta.db_table)

    def db_for_write(self, model, **hints):
        #return self.routeToBase(model._meta.model_name)
        return self.routeToBase(model._meta.db_table)
#metode allow_migrate ir paredzēta, lai noteiktu uz kuru db ir jāmigrē modelis atkarībā no sekojošiem nosacījumiem - vai app_lab (modeļa lietojumprogrammas etiķete) ir sarakstā business_entities vai arī app_label ir ekvivalents ar modeļa nosaukumu, kas sākas ar "a_" vai 'g'. 
#izmanto apakšsvītru, lai atdalītu lietojumprogrammmas etiķeti no modeļa nosaukuma.
    def allow_migrate(self, db, app_label, model_name=None, **hints):
       # print(f"apppl: {app_label}, mdl: {str(model_name)}")
        if app_label in self.business_entities or app_label in ['a', 'g']:
            return db == self.meta_db
        else:
            return db == self.default_db 