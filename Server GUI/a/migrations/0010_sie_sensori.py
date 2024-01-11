from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('a', '0009_alter_measuremeta_range_step'),
    ]

    def insertData(apps, schema_editor):
        Connection_InterfaceMetta = apps.get_model("a", "Connection_InterfaceMeta")
        dht11_22_int, wasnotthere = Connection_InterfaceMetta.objects.get_or_create(
            interface="SPI"
        )
        
        ds18b20_int, wasnotthereds18b20int = Connection_InterfaceMetta.objects.get_or_create(
            interface="1wire"
         )
        twob_int, wasnottheretwo2b = Connection_InterfaceMetta.objects.get_or_create(
            interface="4-20mA"
         )
        MeasureMeta = apps.get_model("a", "MeasureMeta")
        dht11_temp_range, wasnotthere11t = MeasureMeta.objects.get_or_create(
            measurement="t",
             range_low=0,
             range_high=50,
             range_step=2
         )
        
        dht22_temp_range, wasnotthere22t = MeasureMeta.objects.get_or_create(
            measurement="t",
             range_low=-40,
             range_high=125,
             range_step=0.5
         )
        
        dht11_humid_range, wasnotthere11h = MeasureMeta.objects.get_or_create(
            measurement="hum",
             range_low=20,
             range_high=80,
             range_step=5
         )
        dht22_humid_range, wasnotthere22h = MeasureMeta.objects.get_or_create(
            measurement="hum",
             range_low=0,
             range_high=100,
             range_step=5
         )
        ds18b20_temp_range, wasnotthere11t = MeasureMeta.objects.get_or_create(
            measurement="t",
             range_low=-55,
             range_high=125,
             range_step=0.5
         )
        twob_co2_range, wasnottheretwob = MeasureMeta.objects.get_or_create(
            measurement="co2",
             range_low=0,
             range_high=5000,
             range_step=0.5
         )
        HubMeta = apps.get_model("a", "HubMeta")
        h1, wnh1 =    HubMeta.objects.get_or_create(
    nr = 1,
    model = "Raspberry Pi Pico",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "1st hub Raspbrry pi pico RP",
    is_real = True
            )
        h2, wnh2 =    HubMeta.objects.get_or_create(
    nr = 2,
    model = "Raspberry Pi Pico, BluePill",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "2nd hub Raspbrry pi pico RP + BluePill",
    is_real = True
            )
        h3, wnh3 =    HubMeta.objects.get_or_create(
    nr = 3,
    model = "ESP WROVER",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "3rd hub ESP WROVER",
    is_real = True
            )
        h4, wnh4 =    HubMeta.objects.get_or_create(
    nr = 4,
    model = "ESP NODE mcu",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "4th hub ESP NODE mcu",
    is_real = True
            )
        SensorMeta = apps.get_model("a", "SensorMeta")
        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 1,
    hub = h1,
    model = "DHT11",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "DHT11 on RP #22",
    interface = dht11_22_int,
    is_real = True,
            )
        idiotDjangoNoBulk.measurements.add(dht11_temp_range.nr)
        idiotDjangoNoBulk.measurements.add(dht11_humid_range.nr)

        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 3,
    hub = h1,
    model = "DHT22",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "DHT22 on RP #21",
    interface = dht11_22_int,
    is_real = True,
            )
        idiotDjangoNoBulk.measurements.add(dht22_temp_range.nr)
        idiotDjangoNoBulk.measurements.add(dht22_humid_range.nr)

        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 4,
    hub = h1,
    model = "DHT22",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "DHT22 on RP #3",
    interface = dht11_22_int,
    is_real = True,
            )
        
        idiotDjangoNoBulk.measurements.add(dht22_temp_range.nr)
        idiotDjangoNoBulk.measurements.add(dht22_humid_range.nr)

        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 5,
    hub = h1,
    model = "DHT11",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "DHT11 on RP #20",
    interface = dht11_22_int,
    is_real = True,
            )
        idiotDjangoNoBulk.measurements.add(dht11_temp_range.nr)
        idiotDjangoNoBulk.measurements.add(dht11_humid_range.nr)

        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 6,
    hub = h1,
    model = "ds18b20",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "ds18b20 on RP #7",
    interface = ds18b20_int,
    is_real = True,
            )
        idiotDjangoNoBulk.measurements.add(ds18b20_temp_range.nr)

        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 2,
    hub = h2,
    model = "2B",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "2B on RP #UART and Bluepill ADC",
    interface = twob_int,
    is_real = True,
            )
        
        idiotDjangoNoBulk.measurements.add(twob_co2_range.nr)

        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 7,
    hub = h3,
    model = "DHT11",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "DHT11 on ESP WROVER #33",
    interface = dht11_22_int,
    is_real = True,
            )
        
        idiotDjangoNoBulk.measurements.add(dht11_temp_range.nr)
        idiotDjangoNoBulk.measurements.add(dht11_humid_range.nr)

        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 8,
    hub = h3,
    model = "DHT22",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "DHT22 on ESP WROVER #12",
    interface = dht11_22_int,
    is_real = True,
            )
        
        idiotDjangoNoBulk.measurements.add(dht22_temp_range.nr)
        idiotDjangoNoBulk.measurements.add(dht22_humid_range.nr)

        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 9,
    hub = h3,
    model = "DHT22",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "DHT22 on ESP WROVER #13",
    interface = dht11_22_int,
    is_real = True,
            )
        
        idiotDjangoNoBulk.measurements.add(dht22_temp_range.nr)
        idiotDjangoNoBulk.measurements.add(dht22_humid_range.nr)

        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 10,
    hub = h3,
    model = "DHT11",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "DHT11 on ESP WROVER #14",
    interface = dht11_22_int,
    is_real = True,
            )
        
        idiotDjangoNoBulk.measurements.add(dht11_temp_range.nr)
        idiotDjangoNoBulk.measurements.add(dht11_humid_range.nr)

        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 11,
    hub = h3,
    model = "ds18b20",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "ds18b20 on ESP WROVER #32",
    interface = ds18b20_int,
    is_real = True,
            )
        
        idiotDjangoNoBulk.measurements.add(ds18b20_temp_range.nr)

        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 12,
    hub = h4,
    model = "DHT11",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "DHT11 on ESP NODE mcu #4",
    interface = dht11_22_int,
    is_real = True,
            )
        
        idiotDjangoNoBulk.measurements.add(dht11_temp_range.nr)
        idiotDjangoNoBulk.measurements.add(dht11_humid_range.nr)

        idiotDjangoNoBulk = SensorMeta.objects.create(
    nr = 13,
    hub = h4,
    model = "DHT22",
    update_interval = 1,
    loc_la = 56.9518978,
    loc_lo = 24.0777201,
    loc_ro =  1,
    comment = "DHT22 on ESP NODE mcu #5",
    interface = dht11_22_int,
    is_real = True,
            )
        
        idiotDjangoNoBulk.measurements.add(dht22_temp_range.nr)
        idiotDjangoNoBulk.measurements.add(dht22_humid_range.nr)



    operations = [
        migrations.RunPython(insertData),
    ]