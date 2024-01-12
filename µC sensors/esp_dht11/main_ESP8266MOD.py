# at this moment 5 new records appear while waiting for db to write so first 10=> send (+5 in the meanwhile), then @10=>send so it sends each 
#5 measurements instead of intended 10 @1sec interval measuring
#esp.osdebug(None)
debuglevel1 = 0
__DEBUG_LEVEL_1__ = True if debuglevel1==1 else False
debuglevel2 = 0
__DEBUG_LEVEL_2__ = True if debuglevel2==1 else False
import os, machine
#os.dupterm(None, 1) # disable REPL on UART(0)
import gc
import network
import dht
import time
from machine import Pin
import asyncio
import json
import socket
import ntptime
#import onewire, ds18x20
#import webrepl
#webrepl.start()

__MEAS_INTERVAL__ = 4
__MINIMUM_MEASURES_TO_SEND__=10
__MAXIMUM_SECS_BEFORE_SEND__=30
__LED__=2
#__LOOP_DEBUG_LEN__ = 99999
HOSTNAME = 4
HOST = 'jtag.me'  # The server's hostname or IP address
PORT = 911       # Port to connect to
CLI_ID = 12		#device id to send
CLI_ID2 = 13		#device id to send
#CLI_ID3 = 9		#device id to send
#CLI_ID4 = 10		#device id to send
#CLI_ID5 = 9		#device id to send
#, Pin.OUT, Pin.PULL_DOWN)
#sensor = dht.DHT11(Pin(4))
sensor2 = dht.DHT22(Pin(5))
#sensor3 = dht.DHT22(Pin(3))
#sensor4 = dht.DHT11(Pin(4))
#onewire5 = ds18x20.DS18X20(onewire.OneWire(Pin(14)))

#onewire_devs5 = onewire5.scan()
#if(__DEBUG_LEVEL_1__):
#    print('Found DS devices: ', onewire_devs5)

wlan = network.WLAN(network.STA_IF) # create station interface

li_mem_clog = []
li_mem_clog2 = []
#li_mem_clog3 = []
#li_mem_clog4 = []
#li_mem_clog5 = []


def strftime(tup: tuple):
    return "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])

def t(tup: tuple):
    return strftime(tup)

async def tsk_con_net():
    wlan.active(True)       # activate the interface
    #l = wlan.scan()
    #print(l)
    while(True):
        try:
            if not wlan.isconnected():
                wlan.connect("ff", "")
                while not wlan.isconnected():
                    await asyncio.sleep(1)
            ntptime.settime()
            uptime_stamp = time.mktime(time.gmtime())
            return True
        except Exception as e:
            print(f"{t(time.gmtime())} tsk con net {str(e)}")  
    #print('network config:', wlan.ifconfig())

async def measure_interval_updater():
    global __MEAS_INTERVAL__
    while(True):
        try:
            reader, writer = await asyncio.open_connection(HOST, PORT)
            writer.write(f"NET_{HOSTNAME}\n".encode())
            await writer.drain()
            await asyncio.sleep(1)
            response = await reader.read(1024)
            print(f"decoded: {response.decode()}")
            print(f"original: {response}")
            if(int(response)^ord('d') > 0):
                __MEAS_INTERVAL__ = int(response)^ord('d')
            writer.close()
            await writer.wait_closed()
            reader.close()
            await asyncio.sleep(1)
        except Exception as e:
            print(f"{t(time.gmtime())} messaure interval updater: {str(e)}")
            await asyncio.sleep(2)
        
async def push_data_net():
    #global __MEAS_INTERVAL__
    await asyncio.sleep(1)
    try:
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)
        #addr = socket.getaddrinfo(HOST, PORT)[0][-1]
        #s.connect((HOST, PORT))
        reader, writer = await asyncio.open_connection(HOST, PORT)
        #avoid race conds/?? ja nu kas :D
        length = len(li_mem_clog)
        if(__DEBUG_LEVEL_1__):
            print(f'Send 1: {!r}')
        writer.write(json.dumps({"epoch" : time.gmtime(0)[0],
                                 "id": CLI_ID,
                                 "len": length
                                 }).encode() + b'\n')
        writer.write(json.dumps(li_mem_clog[0:length]).encode() + b'\n')
        await writer.drain()
        await asyncio.sleep(1)
        #await s.connect(addr)
        #s.sendall(json.dumps(li_mem_clog[0:length]).encode() + b'\n')
        #s.send(bytes(json.dumps(li_mem_clog[0:length]).encode() + b'\n'), 'utf-8')
        #response = s.recv(1024)
        #print(response)
        response = await reader.read(1024)
        #responsea = str(response.decode()).split(" ")
        #response = responsea[0]
        #if(len(responsea)>1):
        #    q = int(responsea[1])
        #    if(q^ord('d') > 0):
        #        __MEAS_INTERVAL__=q^ord('d')
        #k = await reader.drain()
        if(__DEBUG_LEVEL_1__):
            print('Close the connection 1')
        writer.close()
        await writer.wait_closed()
        reader.close()
        if(int(response) == length):
            del li_mem_clog[0:length]
            await asyncio.sleep(1)
            return
        else:
            if(__DEBUG_LEVEL_1__):
                print(f"{t(time.gmtime())} fail to send 1. response was {response}")
        #s.close()
    except Exception as e:
        print(f"{t(time.gmtime())}  push 1 {str(e)}")      
    print(f"{t(time.gmtime())} failed to sync 1")
    return

async def push_data_net2():
    await asyncio.sleep(1)
    try:
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)
        #addr = socket.getaddrinfo(HOST, PORT)[0][-1]
        #s.connect((HOST, PORT))
        reader, writer = await asyncio.open_connection(HOST, PORT)
        #avoid race conds/?? ja nu kas :D
        length = len(li_mem_clog2)
        if(__DEBUG_LEVEL_1__):
            print(f'Send 2: {!r}')
        writer.write(json.dumps({"epoch" : time.gmtime(0)[0],
                                 "id": CLI_ID2,
                                 "len": length
                                 }).encode() + b'\n')
        writer.write(json.dumps(li_mem_clog2[0:length]).encode() + b'\n')
        await writer.drain()
        await asyncio.sleep(1)
        #await s.connect(addr)
        #s.sendall(json.dumps(li_mem_clog[0:length]).encode() + b'\n')
        #s.send(bytes(json.dumps(li_mem_clog[0:length]).encode() + b'\n'), 'utf-8')
        #response = s.recv(1024)
        #print(response)
        response = await reader.read(1024)
        #k = await reader.drain()
        if(__DEBUG_LEVEL_1__):
            print('Close the connection 2')
        writer.close()
        await writer.wait_closed()
        reader.close()
        if(int(response) == length):
            del li_mem_clog2[0:length]
            await asyncio.sleep(1)
            return
        else:
            if(__DEBUG_LEVEL_1__):
                print(f"{t(time.gmtime())} fail to send 2. response was {response}")
        #s.close()
    except Exception as e:
        print(f"{t(time.gmtime())}  push 2 {str(e)}")      
    print(f"{t(time.gmtime())} failed to sync 2")
    return

__PUSH_DATA_LOCK__ = False
async def push_data():
    if(__PUSH_DATA_LOCK__): return
    __PUSH_DATA_LOCK__ = True
    if not wlan.isconnected():
        await asyncio.sleep(1)
    else:
        if(len(li_mem_clog2) > 0):
            if(len(li_mem_clog2) >= __MINIMUM_MEASURES_TO_SEND__ or time.time()-li_mem_clog2[0][0] >= __MAXIMUM_SECS_BEFORE_SEND__):
            #print(li_mem_clog.pop(0))
            #print(li_mem_clog.pop(0))
                try:
                    #nets = asyncio.create_task(push_data_net())
                    #await asyncio.sleep(0)
                    nets2 = asyncio.create_task(push_data_net2())
                    await asyncio.sleep(1)
                    #nets3 = asyncio.create_task(push_data_net3())
                    #await asyncio.sleep(0)
                    #nets4 = asyncio.create_task(push_data_net4())
                    #await asyncio.sleep(1)
                    #nets5 = asyncio.create_task(push_data_net5())
                    #await asyncio.sleep(0)
                    if(__DEBUG_LEVEL_1__):
                        seccounter = 0
                    while (not nets2.done()):# and not nets2.done()):# and not nets3.done() and not nets4.done() and not nets5.done()):
                        if(__DEBUG_LEVEL_1__):
                            print(f"{t(time.gmtime())} waiting...{seccounter}")
                            seccounter = seccounter +1
                            if(seccounter > 120):
                                return False
                        await asyncio.sleep(1)
                    #nets_w = asyncio.wait_for(nets, 3)
                    #await asyncio.sleep(0)
                    #i = nets.data
                    #for res in i:
                    #    print(res)
                    __PUSH_DATA_LOCK__ = False
                    await asyncio.sleep(1)       
                except Exception as e:
                    __PUSH_DATA_LOCK__ = False
                    print("{t(time.gmtime())} failed to sync all")
                    print(f"{t(time.gmtime())}  push all {e}")
        return True

async def alarm_clock():
    global __MEAS_INTERVAL__
    counter = 0
    while(counter< __MEAS_INTERVAL__):
        await asyncio.sleep(1)
        counter = counter+1
        if(__DEBUG_LEVEL_1__):
            print(f'{t(time.gmtime())} count: {counter} meas: {__MEAS_INTERVAL__}')
    
led_on = False
async def light(howlong):
    global led_on
    if(led_on):
        while(led_on):
            await asyncio.sleep(howlong/2)
    led_on=True
    led = Pin(__LED__, Pin.OUT)
    led.on()
    await asyncio.sleep(howlong)
    led.off()
    led = Pin(__LED__, Pin.IN)
    led_on=False
    
laststates = [False, False, False, False, False]

async def measure(li_mem_clog, push_data, sensor, number, onewire_special):
    print(f"{t(time.gmtime())} {number} init__")
    just_was_exception = False
    global laststates, __MEAS_INTERVAL__
    if(__MEAS_INTERVAL__ > 1):
        waker = asyncio.create_task(alarm_clock())
        await asyncio.sleep(0)
        while (not waker.done()):
            await asyncio.sleep(1)
    else:
        await asyncio.sleep(1)
    while True: #i<__LOOP_DEBUG_LEN__:
        try:
            if(__DEBUG_LEVEL_2__):
                print(f"{t(time.gmtime())} {number} init")
            if len(li_mem_clog) > 54:
                tsk2 = asyncio.create_task(push_data())
                await asyncio.sleep(3)
                continue
            if(onewire_special):
                sensor.convert_temp()
                asyncio.sleep_ms(750)
            else:
                sensor.measure()
            laststates[number-1] = True
            if(__DEBUG_LEVEL_1__):
                print(number)
            if(onewire_special):
                temp = sensor.read_temp(onewire_special)
                if(__DEBUG_LEVEL_2__):
                    print(f"{t(time.gmtime())} {number} t: {temp} hum: n/a")
                li_mem_clog.append([time.mktime(time.gmtime()), temp])
            else:
                temp = sensor.temperature()
                hum = sensor.humidity()
                if(__DEBUG_LEVEL_2__):
                    print(f"{t(time.gmtime())} {number} t: {temp} hum: {hum}")
                li_mem_clog.append([time.mktime(time.gmtime()), temp, hum])
            if(just_was_exception):
                print(f"{t(time.gmtime())} sensor {number} now OK!")
            just_was_exception = False
            laststates[number-1] = False
            if(__MEAS_INTERVAL__ > 1):
                waker = asyncio.create_task(alarm_clock())
                await asyncio.sleep(0)
                while (not waker.done()):
                    await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)
        except OSError as e:
            print(f'{t(time.gmtime())} Sensor {number}: OSerror, probably Failed to read sensor:')
            print(e)
            print(laststates)
            print(t(time.gmtime()))
            just_was_exception = True
            await asyncio.sleep(__MEAS_INTERVAL__+1)
        except Exception as ex:
            print(f'{t(time.gmtime())} Sensor {number}: general exc')
            print(ex)
            print(laststates)
            print(t(time.gmtime()))
            just_was_exception = True
            await asyncio.sleep(__MEAS_INTERVAL__+1)
            
async def main():
    global __MEAS_INTERVAL__
    just_was_exception = False
    
    print(f"{t(time.gmtime())} Welcome! Booting up by connecting to the network")
    tsk = asyncio.create_task(tsk_con_net())
    #shis palaiz tsk!!!11
    await asyncio.sleep(0)
    tsk2 = asyncio.create_task(push_data())
    await asyncio.sleep(0)
    tsk_inter = asyncio.create_task(measure_interval_updater())
    await asyncio.sleep(0)
    #i=0
    if(__DEBUG_LEVEL_2__):
        print(f"{t(time.gmtime())} launch s1")
    #measure_1 = asyncio.create_task(measure(li_mem_clog, push_data, sensor, 1, False))
    #await asyncio.sleep(0)
    if(__DEBUG_LEVEL_2__):
        print(f"{t(time.gmtime())} launch s2")
    measure_2 = asyncio.create_task(measure(li_mem_clog2, push_data, sensor2, 2, False))
    await asyncio.sleep(0)
    #if(__DEBUG_LEVEL_2__):
    #    print(f"{t(time.gmtime())} launch s3")
    #measure_3 = asyncio.create_task(measure(li_mem_clog3, push_data, sensor3, 3, False))
    #await asyncio.sleep(0)
    #if(__DEBUG_LEVEL_2__):
    #    print(f"{t(time.gmtime())} launch s4")
    #measure_4 = asyncio.create_task(measure(li_mem_clog4, push_data, sensor4, 4, False))
    #await asyncio.sleep(0)
    #if(__DEBUG_LEVEL_2__):
    #    print(f"{t(time.gmtime())} launch s5")
    #measure_5 = asyncio.create_task(measure(li_mem_clog5, push_data, onewire5, 5, onewire_devs5[0]))
    #await asyncio.sleep(0)
    
    while True: #i<__LOOP_DEBUG_LEN__:
      try:
        if not wlan.isconnected():
            tsk = asyncio.create_task(tsk_con_net())
            await asyncio.sleep(5)
            continue
        lig = asyncio.create_task(light(1/2))
        await asyncio.sleep(0)
        if(tsk2.done()):
            tsk2 = asyncio.create_task(push_data())
            await asyncio.sleep(0)
        if(__MEAS_INTERVAL__ > 1):
                #waker = asyncio.create_task(alarm_clock(number-1))
            waker = asyncio.create_task(alarm_clock())
            await asyncio.sleep(0)
            while (not waker.done()):
                await asyncio.sleep(1)
        else: await asyncio.sleep_ms(1000)
        #for sensor in onewire_devs5:
        #    print(f"sensor unique address: {sensor}")
        #    print(onewire5.read_temp(sensor))

        if(just_was_exception):
            print(f"{t(time.gmtime())} main now OK!")
        just_was_exception = False
        await asyncio.sleep(__MEAS_INTERVAL__)
        #print(time.localtime())
        #print(json.loads(json.dumps(time.localtime()))[5])
        #print(f'lis1: {len(li_mem_clog)} lis2: {len(li_mem_clog2)} lis3: {len(li_mem_clog3)}')
      except OSError as e:
        print(f'{t(time.gmtime())} Main loop: OSerror, probably Failed to read sensor:')
        print(e)
        print(laststates)
        print(t(time.gmtime()))
        just_was_exception = True
        await asyncio.sleep(__MEAS_INTERVAL__)
      except Exception as ex:
        print(f'{t(time.gmtime())} Main loop Exception:')
        print(ex)
        print(laststates)
        print(t(time.gmtime()))
        just_was_exception = True
        await asyncio.sleep(__MEAS_INTERVAL__)
      #i=i+1

light(2)
#NotImplementedError: attributes not supported
#print("{0[0]}/{0[1]}/{0[2]} {0[3]}:{0[4]}".format(time.gmtime()))
#NotImplementedError: attributes not supported
asyncio.run(main())


