# at this moment 5 new records appear while waiting for db to write so first 10=> send (+5 in the meanwhile), then @10=>send so it sends each 
#5 measurements instead of intended 10 @1sec interval measuring
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
pin = Pin(22)#, Pin.OUT, Pin.PULL_DOWN)
sensor = dht.DHT11(pin)
sensor2 = dht.DHT22(Pin(21))
sensor3 = dht.DHT22(Pin(3))

wlan = network.WLAN(network.STA_IF) # create station interface

li_mem_clog = []
li_mem_clog2 = []
li_mem_clog3 = []

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

async def push_data_net():
    await asyncio.sleep(2)
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
        #k = await reader.drain()
        print('Close the connection')
        writer.close()
        await writer.wait_closed()
        reader.close()
        if(int(response) == length):
            del li_mem_clog[0:length]
            await asyncio.sleep(1)
            return
        #s.close()
    except Exception as e:
        print(str(e))      
    print("failed to sync")
    return

async def push_data_net2():
    await asyncio.sleep(2)
    try:
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)
        #addr = socket.getaddrinfo(HOST, PORT)[0][-1]
        #s.connect((HOST, PORT))
        reader, writer = await asyncio.open_connection(HOST, PORT)
        #avoid race conds/?? ja nu kas :D
        length = len(li_mem_clog2)
        print(f'Send: {!r}')
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
        print('Close the connection')
        writer.close()
        await writer.wait_closed()
        reader.close()
        if(int(response) == length):
            del li_mem_clog2[0:length]
            await asyncio.sleep(1)
            return
        #s.close()
    except Exception as e:
        print(str(e))      
    print("failed to sync")
    return

async def push_data_net3():
    await asyncio.sleep(2)
    try:
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)
        #addr = socket.getaddrinfo(HOST, PORT)[0][-1]
        #s.connect((HOST, PORT))
        reader, writer = await asyncio.open_connection(HOST, PORT)
        #avoid race conds/?? ja nu kas :D
        length = len(li_mem_clog2)
        print(f'Send: {!r}')
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
        print('Close the connection')
        writer.close()
        await writer.wait_closed()
        reader.close()
        if(int(response) == length):
            del li_mem_clog3[0:length]
            await asyncio.sleep(1)
            return
        #s.close()
    except Exception as e:
        print(str(e))      
    print("failed to sync")
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
                    await asyncio.sleep(0)
                    nets3 = asyncio.create_task(push_data_net3())
                    await asyncio.sleep(0)
                    while (not nets.done() and not nets2.done() and not nets3.done()):
                        print("waiting...")
                        await asyncio.sleep(1)
                    #nets_w = asyncio.wait_for(nets, 3)
                    #await asyncio.sleep(0)
                    #i = nets.data
                    #for res in i:
                    #    print(res)
                    await asyncio.sleep(1)       
                except Exception as e:
                    print("failed to sync")
                    print(e)
        return True
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
    print("checking, connecting to network")
    tsk = asyncio.create_task(tsk_con_net())
    #shis palaiz tsk!!!11
    await asyncio.sleep(0)
    tsk2 = asyncio.create_task(push_data())
    await asyncio.sleep(0)
    #i=0
    while True: #i<__LOOP_DEBUG_LEN__:
      try:
        lig = asyncio.create_task(light(__MEAS_INTERVAL__/2))
        #await asyncio.sleep(0)
        await asyncio.sleep(__MEAS_INTERVAL__)
        sensor.measure()
        sensor2.measure()
        sensor3.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        temp2 = sensor2.temperature()
        hum2 = sensor2.humidity()
        temp3 = sensor3.temperature()
        hum3 = sensor3.humidity()
        #print(f'temp1: {temp} temp2: {temp2} temp3: {temp3}')
        #print(f'hum1: {hum} hum2: {hum2} hum3: {hum3}')
        #temp_f = temp * (9/5) + 32.0
        #print(time.gmtime(0)[0])
        #yr, Month, date, h, m, s, weekday, yearday
        li_mem_clog.append([time.mktime(time.gmtime()), temp, hum])
        li_mem_clog2.append([time.mktime(time.gmtime()), temp2, hum2])
        li_mem_clog3.append([time.mktime(time.gmtime()), temp3, hum3])
        #print(time.localtime())
        #print(json.loads(json.dumps(time.localtime()))[5])
        #print('Temperature: %3.1f C' %temp)
        #print('Temperature: %3.1f F' %temp_f)
        #print('Humidity: %3.1f %%' %hum)
        #print(f'lis1: {len(li_mem_clog)} lis2: {len(li_mem_clog2)} lis3: {len(li_mem_clog3)}')
        if(tsk2.done()):
            tsk2 = asyncio.create_task(push_data())
            await asyncio.sleep(0)
      except OSError as e:
        print('Failed to read sensor.')
        print(e)
      #i=i+1

light(2)
asyncio.run(main())



