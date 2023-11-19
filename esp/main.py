# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
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
#import webrepl
#webrepl.start()
gc.collect()

__MEAS_INTERVAL__ = 1
__MINIMUM_MEASURES_TO_SEND__=10
__MAXIMUM_SECS_BEFORE_SEND__=30
__LOOP_DEBUG_LEN__ = 999
HOST = 'jtag.me'  # The server's hostname or IP address
PORT = 911       # Port to connect to
sensor = dht.DHT11(Pin(15))

wlan = network.WLAN(network.STA_IF) # create station interface

li_mem_clog = []

async def tsk_con_net():
    wlan.active(True)       # activate the interface
    #l = wlan.scan()
    #print(l)
    if not wlan.isconnected():
        wlan.connect("ff", "")
        while not wlan.isconnected():
            await asyncio.sleep(1)
    ntptime.settime()
    #print('network config:', wlan.ifconfig())
    return True
a=0
async def push_data_net():
    await asyncio.sleep(2)
    a = 500
    try:
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)
        #addr = socket.getaddrinfo(HOST, PORT)[0][-1]
        #s.connect((HOST, PORT))
        reader, writer = await asyncio.open_connection(HOST, PORT)
        #avoid race conds/?? ja nu kas :D
        length = len(li_mem_clog)
        print(f'Send: {!r}')
        writer.write(json.dumps({"epoch" : time.gmtime(0)[0],
                                 "id": 1,
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
        #k = await reader.drain()
        print('Close the connection')
        writer.close()
        await writer.wait_closed()
        reader.close()
        if(int(response) == length):
            del li_mem_clog[0:length]
            a = 200
        #s.close()
    except Exception as e:
        print(str(e))      
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
                    a = 0
                    nets = asyncio.create_task(push_data_net())
                    await asyncio.sleep(0)
                    while (not nets.done()):
                        print("waiting...")
                        await asyncio.sleep(1)
                    #nets_w = asyncio.wait_for(nets, 3)
                    #await asyncio.sleep(0)
                    #i = nets.data
                    #for res in i:
                    #    print(res)
                    if(a!=200):
                        print("failed to sync")
                except Exception as e:
                    print("failed to sync")
                    print(e)
        return True

async def light(howlong):
    led = Pin(2, Pin.OUT)
    await asyncio.sleep(howlong)
    led = Pin(2, Pin.IN)

async def main():
    print("checking, connecting to network")
    tsk = asyncio.create_task(tsk_con_net())
    #shis palaiz tsk!!!11
    await asyncio.sleep(0)
    lig = asyncio.create_task(light(1))
    await asyncio.sleep(0)
    tsk2 = asyncio.create_task(push_data())
    await asyncio.sleep(0)
    i=0
    while i<__LOOP_DEBUG_LEN__:
      try:
        led = Pin(2, Pin.OUT)
        await asyncio.sleep(__MEAS_INTERVAL__)
        led = Pin(2, Pin.IN)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        #temp_f = temp * (9/5) + 32.0
        #print(time.gmtime(0)[0])
        #yr, Month, date, h, m, s, weekday, yearday
        li_mem_clog.append([time.mktime(time.gmtime()), temp, hum])
        #print(time.localtime())
        #print(json.loads(json.dumps(time.localtime()))[5])
        #print('Temperature: %3.1f C' %temp)
        #print('Temperature: %3.1f F' %temp_f)
        #print('Humidity: %3.1f %%' %hum)
        print(len(li_mem_clog))
        if(tsk2.done()):
            tsk2 = asyncio.create_task(push_data())
            await asyncio.sleep(0)
      except OSError as e:
        print('Failed to read sensor.')
        print(e)
      i=i+1

led = Pin(2, Pin.OUT)
time.sleep(1)
led = Pin(2, Pin.IN)
asyncio.run(main())


