from django.db import models as m
from django.core.validators import MinValueValidator, MaxValueValidator

class HubMeta(m.Model):
    nr = m.BigAutoField(primary_key=True, default=None)
    model = m.CharField(max_length=127)
    #sensors = m.ManyToManyField('SensorMeta')
    loc_la = m.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0),])
    loc_lo = m.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0),])
    loc_ro = m.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999),])
    comment = m.TextField(null=True)
    hub = m.ForeignKey('self', null=True, blank=True, on_delete=m.SET_NULL)
    update_interval = m.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3600),], default=1)
    is_real = m.BooleanField(default=False)
    def __str__(s):
        wsgi_error = f"; parent: [{s.hub.nr}]" if s.hub else ""
        wsgi_err_f_string_expecting = s.loc_ro if s.loc_ro else "???"
        wsgi_wtf = "_F_ " if not s.is_real else ""
        return f"{wsgi_wtf }hub: [{s.nr}] {s.model}; r: ({wsgi_err_f_string_expecting}){wsgi_error}"

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
        ("1wire", "1wire"),
    ]
    interface = m.CharField(max_length=30,choices=the_interfaces_enum)
    
    def __str__(s):
        return f"[{s.nr}] {s.interface}"

class SensorMeta(m.Model):
    nr = m.BigAutoField(primary_key=True, default=None)
    model = m.CharField(max_length=127)
    #hubs = m.ManyToManyField('HubMeta')
    hub = m.ForeignKey(HubMeta, null=True, on_delete=m.SET_NULL)
    interface = m.ForeignKey(Connection_InterfaceMeta, null=True, on_delete=m.SET_NULL)
    measurements = m.ManyToManyField('MeasureMeta')
    update_interval = m.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3600),], default=1)
    loc_la = m.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0),])
    loc_lo = m.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0),])
    loc_ro = m.SmallIntegerField( validators=[MinValueValidator(1), MaxValueValidator(999),])
    comment = m.TextField(null=True)
    is_real = m.BooleanField(default=False)
    def __str__(s):
        wsgi_wtf = "_F_ " if not s.is_real else ""
        wsgi_cant_bear_tenary = s.loc_ro if s.loc_ro else "???"
        wsgi_oh_no = f" at {s.interface.interface}" if s.interface else ""
        return f"{wsgi_wtf }sens: [{s.nr}] {s.model}; r: ({wsgi_cant_bear_tenary}); hub: [{s.hub.nr}]{wsgi_oh_no}"

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
    #range_step = m.DecimalField(max_digits=20, decimal_places=5, default=0.00001,
    #                            validators=[MinValueValidator(range_low.to_python()), MaxValueValidator(range_high.to_python()),])
    range_step = m.DecimalField(max_digits=20, decimal_places=5, default=0.00001,
                                validators=[MinValueValidator(0)])

    def __str__(s):
        return f"{s.measurement}: {s.range_low} : {s.range_high}"
    
    class Meta:
        constraints = [
            m.UniqueConstraint(fields=['measurement', 'range_low', 'range_high', 'range_step'], name='measure_pk')
        ]