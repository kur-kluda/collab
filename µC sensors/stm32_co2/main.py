debuglevel1 = 0
__DEBUG_LEVEL_1__ = True if debuglevel1==1 else False
debuglevel1pp = 0
__DEBUG_LEVEL_1pp__ = True if debuglevel1pp==1 else False
debuglevel2 = 0
__DEBUG_LEVEL_2__ = True if debuglevel1==1 else False
import os, machine
#os.dupterm(None, 1) # disable REPL on UART(0)
import gc
import network
import dht
#import time
from machine import Pin
from machine import I2C
import asyncio
import json
import socket
import ntptime
import time
#import busio

#import adafruit_ccs811
#import adafruit_dht

__MEAS_INTERVAL__ = 1
__MINIMUM_MEASURES_TO_SEND__=10
__MAXIMUM_SECS_BEFORE_SEND__=20
#__LOOP_DEBUG_LEN__ = 999
HOSTNAME= 2
__LED__='LED'
HOST = 'jtag.me'  # The server's hostname or IP address
PORT = 912       # Port to connect to
CLI_ID = 2

uptime_stamp = time.mktime(time.gmtime())

wlan = network.WLAN(network.STA_IF) # create station interface

li_mem_clog = []

def strftime(tup: tuple):
    return "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])

def t(tup: tuple):
    return strftime(tup)

__STATUS_CONNECTING__ = False
async def tsk_con_net():
    global __STATUS_CONNECTING__
    if(__STATUS_CONNECTING__): return
    __STATUS_CONNECTING__ = True
    global uptime_stamp
    wlan.active(True)       # activate the interface
    #l = wlan.scan()
    #print(l)
    while(True):
        try:
            if not wlan.isconnected():
                wlan.connect("ff", "")
                while not wlan.isconnected():
                    await asyncio.sleep(1)
            __STATUS_CONNECTING__ = False
            ntptime.settime()
            uptime_stamp = time.mktime(time.gmtime())
            return True
        except Exception as e:
            print(f"{t(time.gmtime())} tsk con net {str(e)}")
            await asyncio.sleep(1)
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
            if(int(response)^ord('d') > 0):
                __MEAS_INTERVAL__ = int(response)^ord('d')
            writer.close()
            await writer.wait_closed()
            reader.close()
            await asyncio.sleep(3)
        except Exception as e:
            print(f"{t(time.gmtime())} meaure interval updater: {str(e)}")
            await asyncio.sleep(2)
            
async def alarm_clock():
    global __MEAS_INTERVAL__
    counter = 0
    while(counter< __MEAS_INTERVAL__):
        await asyncio.sleep(1)
        counter = counter+1
        if(__DEBUG_LEVEL_1__):
            print(f'count: {counter} meas: {__MEAS_INTERVAL__}')

async def push_data_net():
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
            print(f'pd Send: {!r}')
        writer.write(json.dumps({"epoch" : time.gmtime(0)[0],
                                 "id": CLI_ID,
                                 "len": length
                                 }).encode() + b'\n')
        writer.write(json.dumps(li_mem_clog[0:length]).encode() + b'\n')
        await writer.drain()
        await asyncio.sleep(1)
        response = await reader.read(1024)
        #k = await reader.drain()
        if(__DEBUG_LEVEL_1__):
            print(f'{t(time.gmtime())}  pd Close the connection')
        writer.close()
        await writer.wait_closed()
        reader.close()
        if(int(response) == length):
            del li_mem_clog[0:length]
            await asyncio.sleep(1)
            return
        #s.close()
    except Exception as e:
        print(f"{t(time.gmtime())}  push 1 {str(e)}")      
    print("{t(time.gmtime())} failed to sync 1")
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
                    seccounter = 0
                    while (not nets.done()):
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
                    await asyncio.sleep(1)       
                except Exception as e:
                    print("{t(time.gmtime())} failed to sync all")
                    print(f"{t(time.gmtime())}  push all {e}")
        return True


led_on = False
async def light(howlong):
    global led_on
    if(led_on):
        cnt = 0
        while(led_on):
            await asyncio.sleep(howlong/2)
            cnt = cnt+1
            if(cnt>20): return
    led_on=True
    led = Pin(__LED__, Pin.OUT)
    led.on()
    await asyncio.sleep(howlong)
    led.off()
    led = Pin(__LED__, Pin.IN)
    led_on=False
    

async def lineparser(uart):
    while(True):
        await asyncio.sleep(0.1)
        """if uart.any():
                while(not uart.
                d = uart.readline()
                while(d!=None):
                    print("Received:", d)
                    print(d.decode())
                    print(json.loads(d)[0])
                    li_mem_clog.append([time.mktime(time.gmtime()), d[0], d[1]])
                    d = uart.readline()
                    print(d)
                    """
        try:
            reader = asyncio.StreamReader(uart)
            while(True):
                d = await reader.readline()
                if not d:
                    await asyncio.sleep(0.3)
                    continue
                if(__DEBUG_LEVEL_1__):
                    print("Received:", d)
                    print(d.decode())
                arr = json.loads(d)
                if(__DEBUG_LEVEL_1pp__):
                    print(arr[0])
                li_mem_clog.append([time.mktime(time.gmtime()), arr[0], arr[1]])
        except Exception as ex:
            print(f'{t(time.gmtime())} Fail to read UART {str(ex)}')
            await asyncio.sleep(1)

async def main():
    global __MEAS_INTERVAL__
    uart = machine.UART(1, baudrate=9600, tx=Pin('GP4'), rx=Pin('GP5'))  # UART1, GP0 (TX) and GP1 (RX)
    parser = asyncio.create_task(lineparser(uart))
    await asyncio.sleep(0)
    print("checking, connecting to network")
    tsk = asyncio.create_task(tsk_con_net())
    #shis palaiz tsk!!!11
    await asyncio.sleep(0)
    tsk2 = asyncio.create_task(push_data())
    await asyncio.sleep(0)
    tsk_inter = asyncio.create_task(measure_interval_updater())
    await asyncio.sleep(0)

    while True :
      try:
        if not wlan.isconnected():
            tsk = asyncio.create_task(tsk_con_net())
            await asyncio.sleep(5)
            continue
        if(__MEAS_INTERVAL__ > 1):
            waker = asyncio.create_task(alarm_clock())
            await asyncio.sleep(0)
            while (not waker.done()):
                await asyncio.sleep(1)
        else:
            await asyncio.sleep(1)
        if len(li_mem_clog) >230 :
            await asyncio.sleep(1)
            continue
        asyncio.create_task(light(__MEAS_INTERVAL__/2))
        await asyncio.sleep(0)
        if(tsk2.done()):
            tsk2 = asyncio.create_task(push_data())
            await asyncio.sleep(0)
        if(parser.done()):  
            parser = asyncio.create_task(lineparser(uart))
            await asyncio.sleep(0)
      except OSError as e:
        print('{t(time.gmtime())} Main loop: OSerror, probably Failed to read sensor:')
        print(e)

light(2)
asyncio.run(main())
