from django.db import models as m

class HubMeta(m.Model):
    model = m.CharField(max_length=255)
    #sensors = m.ManyToManyField('SensorMeta')
    loc_la = m.FloatField()
    loc_lo = m.FloatField()
    loc_ro = m.FloatField()
    hub = m.ForeignKey('self', null=True, blank=True, on_delete=m.SET_NULL)
    is_real = m.BooleanField(default=False)

class SensorMeta(m.Model):
    the_measure_enum=[
        ('t', 'Temperature'),
        ('hum', 'Humidity'),
        ('tvoc', 'Total Voilatile Component'),
        ('co2', 'Carbon Dioxide'),
        ('p', 'Pressure'),
        ('li', 'Light'),
        ('snd', 'Sound'),
        ('mot', 'Motion')
    ]
    the_interfaces_enum=[
        ("SPI", "SPI"),
        ("JTAG", "JTAG"),
        ("UART", "UART"),
        ("Bluetooth BLE", "Bluetooth BLE"),
        ("WiFi", "WiFi"),
        ("4-20mA", "4-20mA"),
        ("MODBUS", "MODBUS"),
    ]
    model = m.CharField(max_length=255)
    measurements = m.CharField(max_length=5, choices=the_measure_enum)
    ranges = m.JSONField()
    #hubs = m.ManyToManyField('HubMeta')
    hub = m.ForeignKey(HubMeta, on_delete=m.CASCADE)
    interface = m.CharField(max_length=20,choices=the_interfaces_enum)
    loc_la = m.FloatField()
    loc_lo = m.FloatField()
    loc_ro = m.FloatField()
    is_real = m.BooleanField(default=False)
