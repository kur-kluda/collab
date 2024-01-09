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
import onewire, ds18x20
#import webrepl
#webrepl.start()

__MEAS_INTERVAL__ = 1
__MINIMUM_MEASURES_TO_SEND__=10
__MAXIMUM_SECS_BEFORE_SEND__=30
__LED__='LED'
#__LOOP_DEBUG_LEN__ = 99999
HOST = 'jtag.me'  # The server's hostname or IP address
PORT = 911       # Port to connect to
CLI_ID = 1		#device id to send
CLI_ID2 = 3		#device id to send
CLI_ID3 = 4		#device id to send
CLI_ID4 = 5		#device id to send
CLI_ID5 = 6		#device id to send
pin = Pin(22)#, Pin.OUT, Pin.PULL_DOWN)
sensor = dht.DHT11(pin)
sensor2 = dht.DHT22(Pin(21))
sensor3 = dht.DHT22(Pin(3))
sensor4 = dht.DHT11(Pin(20))
onewire5 = ds18x20.DS18X20(onewire.OneWire(Pin(7)))

onewire_devs5 = onewire5.scan()
if(__DEBUG_LEVEL_1__):
    print('Found DS devices: ', onewire_devs5)

wlan = network.WLAN(network.STA_IF) # create station interface

li_mem_clog = []
li_mem_clog2 = []
li_mem_clog3 = []
li_mem_clog4 = []
li_mem_clog5 = []

__STATUS_CONNECTING__ = False
async def tsk_con_net():
    global __STATUS_CONNECTING__
    if(__STATUS_CONNECTING__): return
    __STATUS_CONNECTING__ = True
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
            __STATUS_CONNECTING__ = False
            return True
        except Exception as e:
            print(f"tsk con net {str(e)}")
            await asyncio.sleep(1)
    #print('network config:', wlan.ifconfig())

async def measure_interval_updater():
    global __MEAS_INTERVAL__
    while(True):
        try:
            reader, writer = await asyncio.open_connection(HOST, PORT)
            writer.write("NET\n".encode())
            await writer.drain()
            await asyncio.sleep(1)
            response = await reader.read(1024)
            if(int(response)^ord('d') > 0):
                __MEAS_INTERVAL__ = int(response)^ord('d')
            writer.close()
            await writer.wait_closed()
            reader.close()
            await asyncio.sleep(1)
        except Exception as e:
            print(f"meaure interval updater: {str(e)}")
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
                print(f"fail to send 1. response was {response}")
        #s.close()
    except Exception as e:
        print(f" push 1 {str(e)}")      
    print("failed to sync 1")
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
                print(f"fail to send 2. response was {response}")
        #s.close()
    except Exception as e:
        print(f" push 2 {str(e)}")      
    print("failed to sync 2")
    return

async def push_data_net3():
    await asyncio.sleep(1)
    try:
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)
        #addr = socket.getaddrinfo(HOST, PORT)[0][-1]
        #s.connect((HOST, PORT))
        reader, writer = await asyncio.open_connection(HOST, PORT)
        #avoid race conds/?? ja nu kas :D
        length = len(li_mem_clog3)
        if(__DEBUG_LEVEL_1__):
            print(f'Send 3: {!r}')
        writer.write(json.dumps({"epoch" : time.gmtime(0)[0],
                                 "id": CLI_ID3,
                                 "len": length
                                 }).encode() + b'\n')
        writer.write(json.dumps(li_mem_clog3[0:length]).encode() + b'\n')
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
            print('Close the connection 3')
        writer.close()
        await writer.wait_closed()
        reader.close()
        if(int(response) == length):
            del li_mem_clog3[0:length]
            await asyncio.sleep(1)
            return
        else:
            if(__DEBUG_LEVEL_1__):
                print(f"fail to send 3. response was {response}")
        #s.close()
    except Exception as e:
        print(f" push 3 {str(e)}")      
    print("failed to sync 3")
    return

async def push_data_net4():
    await asyncio.sleep(1)
    try:
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)
        #addr = socket.getaddrinfo(HOST, PORT)[0][-1]
        #s.connect((HOST, PORT))
        reader, writer = await asyncio.open_connection(HOST, PORT)
        #avoid race conds/?? ja nu kas :D
        length = len(li_mem_clog4)
        if(__DEBUG_LEVEL_1__):
            print(f'Send 4: {!r}')
        writer.write(json.dumps({"epoch" : time.gmtime(0)[0],
                                 "id": CLI_ID4,
                                 "len": length
                                 }).encode() + b'\n')
        writer.write(json.dumps(li_mem_clog4[0:length]).encode() + b'\n')
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
            print('Close the connection 4')
        writer.close()
        await writer.wait_closed()
        reader.close()
        if(int(response) == length):
            del li_mem_clog4[0:length]
            await asyncio.sleep(1)
            return
        else:
            if(__DEBUG_LEVEL_1__):
                print(f"fail to send 4. response was {response}")
        #s.close()
    except Exception as e:
        print(f" push 4 {str(e)}")
        #print(li_mem_clog4)
    print("failed to sync 4")
    return

async def push_data_net5():
    await asyncio.sleep(1)
    try:
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)
        #addr = socket.getaddrinfo(HOST, PORT)[0][-1]
        #s.connect((HOST, PORT))
        if(__DEBUG_LEVEL_2__):
            print("aa 0")
        reader, writer = await asyncio.open_connection(HOST, PORT)
        if(__DEBUG_LEVEL_2__):
            print("aa 1")
        #avoid race conds/?? ja nu kas :D
        length = len(li_mem_clog5)
        if(__DEBUG_LEVEL_2__):
            print("aa 2")
        if(__DEBUG_LEVEL_1__):
            print(f'Send 5: {!r}')
        writer.write(json.dumps({"epoch" : time.gmtime(0)[0],
                                 "id": CLI_ID5,
                                 "len": length
                                 }).encode() + b'\n')
        writer.write(json.dumps(li_mem_clog5[0:length]).encode() + b'\n')
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
            print('Close the connection 5')
        writer.close()
        await writer.wait_closed()
        reader.close()
        if(int(response) == length):
            del li_mem_clog5[0:length]
            await asyncio.sleep(1)
            return
        else:
            if(__DEBUG_LEVEL_1__):
                print(f"fail to send 5. response was {response}")
        #s.close()
    except Exception as e:
        print(f" push 5 {str(e)}")      
    print("failed to sync 5")
    return

async def push_data():
    if not wlan.isconnected():
        await asyncio.sleep(1)
    else:
        if(len(li_mem_clog) > 0):
            if(len(li_mem_clog) >= __MINIMUM_MEASURES_TO_SEND__ or time.time()-li_mem_clog[0][0] >= __MAXIMUM_SECS_BEFORE_SEND__):
            #print(li_mem_clog.pop(0))
            #print(li_mem_clog.pop(0))
                try:
                    nets = asyncio.create_task(push_data_net())
                    await asyncio.sleep(0)
                    nets2 = asyncio.create_task(push_data_net2())
                    await asyncio.sleep(1)
                    nets3 = asyncio.create_task(push_data_net3())
                    await asyncio.sleep(0)
                    nets4 = asyncio.create_task(push_data_net4())
                    await asyncio.sleep(1)
                    nets5 = asyncio.create_task(push_data_net5())
                    await asyncio.sleep(0)
                    if(__DEBUG_LEVEL_1__):
                        seccounter = 0
                    while (not nets.done() and not nets2.done() and not nets3.done() and not nets4.done() and not nets5.done()):
                        if(__DEBUG_LEVEL_1__):
                            print(f"waiting...{seccounter}")
                            seccounter = seccounter +1
                            if(seccounter > 120):
                                return False
                        await asyncio.sleep(1)
                    #nets_w = asyncio.wait_for(nets, 3)
                    #await asyncio.sleep(0)
                    #i = nets.data
                    #for res in i:
                    #    print(res)
                    await asyncio.sleep(1)       
                except Exception as e:
                    print("failed to sync all")
                    print(f" push all {e}")
        return True

async def alarm_clock():
    global __MEAS_INTERVAL__
    counter = 0
    while(counter< __MEAS_INTERVAL__):
        await asyncio.sleep(1)
        counter = counter+1
        if(__DEBUG_LEVEL_1__):
            print(f'count: {counter} meas: {__MEAS_INTERVAL__}')
    
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

async def main():
    global __MEAS_INTERVAL__
    print("Welcome! Booting up by connecting to the network")
    tsk = asyncio.create_task(tsk_con_net())
    #shis palaiz tsk!!!11
    await asyncio.sleep(0)
    tsk2 = asyncio.create_task(push_data())
    await asyncio.sleep(0)
    tsk_inter = asyncio.create_task(measure_interval_updater())
    await asyncio.sleep(0)
    #i=0
    while True: #i<__LOOP_DEBUG_LEN__:
      try:
        if not wlan.isconnected():
            tsk = asyncio.create_task(tsk_con_net())
            await asyncio.sleep(0)
            lig = asyncio.create_task(light(1/2))
            await asyncio.sleep(0)
            await asyncio.sleep(2)
            continue
        lig = asyncio.create_task(light(1/2))
        await asyncio.sleep(0)
        if(tsk2.done()):
            tsk2 = asyncio.create_task(push_data())
            await asyncio.sleep(0)
        if len(li_mem_clog) > 64:
            tsk2 = asyncio.create_task(push_data())
            await asyncio.sleep(3)
            lg = asyncio.create_task(light(1/2))
            await asyncio.sleep(0)
            continue
        #await asyncio.sleep(0)
        #print(__MEAS_INTERVAL__)
        # why not this::::
        #await alarm_clock()
        if(__MEAS_INTERVAL__ > 1):
            waker = asyncio.create_task(alarm_clock())
            await asyncio.sleep(0)
            while (not waker.done()):
                await asyncio.sleep(1)
        else:
            await asyncio.sleep(1)
        sensor.measure()
        if(__DEBUG_LEVEL_1__):
            print("1")
        sensor2.measure()
        if(__DEBUG_LEVEL_1__):
            print("2")
        sensor3.measure()
        if(__DEBUG_LEVEL_1__):
            print("3")
        sensor4.measure()
        if(__DEBUG_LEVEL_1__):
            print("4")
        onewire5.convert_temp()
        asyncio.sleep_ms(750)
        #for sensor in onewire_devs5:
        #    print(f"sensor unique address: {sensor}")
        #    print(onewire5.read_temp(sensor))
        temp5 = onewire5.read_temp(onewire_devs5[0])
        if(__DEBUG_LEVEL_1__):
            print("5")
        if(__DEBUG_LEVEL_2__):
            print(f"5 t: {temp5} hum: {'n/a'}")
        temp = sensor.temperature()
        hum = sensor.humidity()
        if(__DEBUG_LEVEL_2__):
            print(f"1 t: {temp} hum: {hum}")
        temp2 = sensor2.temperature()
        hum2 = sensor2.humidity()
        if(__DEBUG_LEVEL_2__):
            print(f"2 t: {temp2} hum: {hum2}")
        temp3 = sensor3.temperature()
        hum3 = sensor3.humidity()
        if(__DEBUG_LEVEL_2__):
            print(f"3 t: {temp3} hum: {hum3}")
        temp4 = sensor4.temperature()
        hum4 = sensor4.humidity()
        if(__DEBUG_LEVEL_2__):
            print(f"4 t: {temp4} hum: {hum4}")
        # 5 is onewire with only temperature and another kind of flow...
        #print(f'temp1: {temp} temp2: {temp2} temp3: {temp3}')
        #print(f'hum1: {hum} hum2: {hum2} hum3: {hum3}')
        #temp_f = temp * (9/5) + 32.0
        #print(time.gmtime(0)[0])
        #yr, Month, date, h, m, s, weekday, yearday
        li_mem_clog.append([time.mktime(time.gmtime()), temp, hum])
        li_mem_clog2.append([time.mktime(time.gmtime()), temp2, hum2])
        li_mem_clog3.append([time.mktime(time.gmtime()), temp3, hum3])
        li_mem_clog4.append([time.mktime(time.gmtime()), temp4, hum4])
        li_mem_clog5.append([time.mktime(time.gmtime()), temp5])
        #print(time.localtime())
        #print(json.loads(json.dumps(time.localtime()))[5])
        #print('Temperature: %3.1f C' %temp)
        #print('Temperature: %3.1f F' %temp_f)
        #print('Humidity: %3.1f %%' %hum)
        #print(f'lis1: {len(li_mem_clog)} lis2: {len(li_mem_clog2)} lis3: {len(li_mem_clog3)}')
      except OSError as e:
        print('Main loop: Oserror, prob Failed to read sensor.')
        print(e)
        await asyncio.sleep(1)
      except Exception as ex:
        print('Main loop Exception:')
        print(ex)
        await asyncio.sleep(1)
      #i=i+1

light(2)
asyncio.run(main())
