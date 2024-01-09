from django.db import models as m
from django.core.validators import MinValueValidator, MaxValueValidator

class HubMeta(m.Model):
    nr = m.BigAutoField(primary_key=True, default=None)
    model = m.CharField(max_length=127)
    #sensors = m.ManyToManyField('SensorMeta')
    loc_la = m.FloatField()
    loc_lo = m.FloatField()
    loc_ro = m.FloatField( validators=[MinValueValidator(1), MaxValueValidator(999),])
    comment = m.TextField(null=True)
    hub = m.ForeignKey('self', null=True, blank=True, on_delete=m.SET_NULL)
    is_real = m.BooleanField(default=False)
    def __str__(s):
        return f"{"_F_ " if not s.is_real else "" }hub: [{s.nr}] {s.model}; r: ({s.loc_ro if s.loc_ro else "???"}){"; parent: [{s.hub.nr}]" if s.hub else ""}"

class Connection_InterfaceMeta(m.Model):
    nr = m.AutoField(primary_key=True, default=None)
    the_interfaces_enum=[
        ("SPI", "SPI"),
        ("JTAG", "JTAG"),
        ("UART", "UART"),
        ("Bluetooth BLE", "Bluetooth BLE"),
        ("WiFi", "WiFi"),
        ("4-20mA", "4-20mA"),
        ("MODBUS", "MODBUS"),
    ]
    interface = m.CharField(max_length=30,choices=the_interfaces_enum)
    
    def __str__(s):
        return f"[{s.nr}] {s.interface}"

class SensorMeta(m.Model):
    nr = m.BigAutoField(primary_key=True, default=None)
    model = m.CharField(max_length=127)
    #hubs = m.ManyToManyField('HubMeta')
    hub = m.ForeignKey(HubMeta, on_delete=m.CASCADE)
    interface = m.ForeignKey(Connection_InterfaceMeta, null=True, on_delete=m.SET_NULL)
    measurements = m.ManyToManyField('MeasureMeta')
    loc_la = m.FloatField()
    loc_lo = m.FloatField()
    loc_ro = m.FloatField( validators=[MinValueValidator(1), MaxValueValidator(999),])
    comment = m.TextField(null=True)
    is_real = m.BooleanField(default=False)
    def __str__(s):
        return f"{"_F_ " if not s.is_real else "" }sens: [{s.nr}] {s.model}; r: ({s.loc_ro if s.loc_ro else "???"}); hub: [{s.hub.nr}]{" at {s.interface.interface}" if s.interface else ""}"

class MeasureMeta(m.Model):
    nr = m.AutoField(primary_key=True, default=None)
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
    measurement = m.CharField(max_length=5, choices=the_measure_enum)
    range_low = m.DecimalField(max_digits=20, decimal_places=5)
    range_high = m.DecimalField(max_digits=20, decimal_places=5)
    def __str__(s):
        return f"{s.measurement}: {s.range_low} : {s.range_high}"
    
    class Meta:
        constraints = [
            m.UniqueConstraint(fields=['measurement', 'range_low', 'range_high'], name='measure_pk')
        ]