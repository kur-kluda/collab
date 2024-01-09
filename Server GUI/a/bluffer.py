from django.shortcuts import render
from django.template import loader
from django.http import request
from . import models as m
import random as r

def gen_recs(n: int):
    sensnames=[
"DS18B20",
"TMP36",
"LM35",
"DHT11",
"DHT22",
"DS3231",
"MLX90614",
"DHT11",
"DHT22",
"HIH-4030",
"HIH-6130",
"SHT15",
"HDC1080",
"MH-Z19",
"MG811",
"CCS811",
"CCS811",
"MiCS-5524",
"CCS811",
"MiCS-5524",
"MQ-135",
"LDR",
"BH1750",
"TSL2561",
"APDS-9301",
"KY-037",
"MAX4466",
"PIR",
"HC-SR501",
"ADXL345",
"BMP180",
"BMP280",
"BMP388",
"MS5611",
"MQ-7",
"MQ-2",
"MiCS-5524",
    ]
    hubnames=[
"ESP8266",
"ESP32",
"nRF52832",
"nRF52840",
"BlueNRG-2",
"CC26xx",
"CC32xx",
"RN4870",
"RN4871",
"ATmega4808",
"ATmega4809",
"EFR32",
"STM32WB",
"Raspberry Pi 3",
"Raspberry Pi 4",
"BeagleBone Black Wireless",
"Odroid-C4",
"NanoPi M4V2",
"Pine64 RockPro64",
"Banana Pi M4",
"Asus Tinker Board S",
"Orange Pi Zero Plus 2 H5",
"Udoo Bolt V8",
"LattePanda Alpha",
"FriendlyElec NanoPi NEO Air",
"Khadas VIM3L",    
]
    is_first_init=False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ create the interface (connection) enum
    if(n>0):
        if(not m.Connection_InterfaceMeta.objects.exists()):
            is_first_init = True
            for i in range(len(m.Connection_InterfaceMeta.the_interfaces_enum)):
            #init the enum
                f = m.Connection_InterfaceMeta(
                interface=m.Connection_InterfaceMeta.the_interfaces_enum[i][0]
                )
                f.save()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ if enum was not there, also create some ranges of measurements
    q = n if n<30 else n//10
    if not is_first_init: q=0
    for i in range(q):
        while True:
            try:

                el = r.randint(0, len(m.MeasureMeta.the_measure_enum))
                low = r.randint(-500, 3000)
                high = r.randint(-400, 30000)
                while(low>=high):
                    high = r.randint(-400, 30000)
                f = m.MeasureMeta(
                    measurement = m.MeasureMeta.the_measure_enum[el][0],
                    range_high = high,
                    range_low = low,

                )
                f.save()
                break
            except Exception as e:
                print(f"exceptedion {e}")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ now single level hubs.
    q = n if n<5 else n//5
    hubslist=[]
    for i in range(q):
        mdlname = hubnames[r.randint(0, len(hubnames)-1)]
        room = r.randint(100, 999)
        h = m.HubMeta(
            model=mdlname,
            #loc_la = r.randrange(-90.0, 90.0, 0.0001),
            loc_la = round(r.uniform(-90.0, 90.0), 5),
            #loc_lo = r.randrange(-180.0, 180.0, 0.0001),
            loc_lo = round(r.uniform(-180.0, 180.0), 5),
            loc_ro = room,
            comment = f"{mdlname} at room {room}",
        )
        h.save()
        hubslist.append(h)
#aaaand finally the sensors themselves
    #interfacelen = m.Connection_InterfaceMeta.objects.count()
    interfaceidsq = m.Connection_InterfaceMeta.objects.values_list('nr', flat=True)
    interfaceids = list(interfaceidsq)
    measurementsidsq = m.MeasureMeta.objects.values_list('nr', flat=True)
    measurementsids = list(measurementsidsq)
    for i in range (n):
        mdlname = sensnames[r.randint(0, len(sensnames)-1)]
        room = r.randint(100, 999)
        sen = m.SensorMeta(
            model = mdlname,
            hub = hubslist[r.randint(0, len(hubslist)-1)],
            interface = m.Connection_InterfaceMeta.objects.get(nr=interfaceids[r.randint(0, len(interfaceids)-1)]),
            loc_la = round(r.uniform(-90.0, 90.0), 5),
            loc_lo = round(r.uniform(-180.0, 180.0), 5),
            loc_ro = room,
            comment = f"{mdlname} at room {room}",
        )
        sen.save()
        abilities_len = r.randint(1, 5)
        meas_ids =[]
        for i in range(abilities_len):
            meas_ids.append(measurementsids[r.randint(0, len(measurementsids)-1)])
            #uniques only pls
        endids = list(set(meas_ids))
        sen.measurements.add(*endids)
        sen.save()
        


def render_bluff(r: request):
    g = r.GET.get("s")
    if(g):
        if(str(g).lower()=="django"):
            num=r.GET.get("n", '-200')
            try:
                num = int(num)
            except ValueError:
                num = 0
            if(num==-200 or num <1):
                g = "show me the <b>n</b>umber bro.."
            else:
                gen_recs(num)
                g= f"{num} exceptionally highly trained smart monkeys have been dispatched. Come again."
        else:
            g = None
    view_model = {
        'is_ok': g
    }
    return render(r, 'bluffer.html', view_model)