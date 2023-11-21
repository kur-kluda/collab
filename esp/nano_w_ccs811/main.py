# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
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
__MAXIMUM_SECS_BEFORE_SEND__=30
__LOOP_DEBUG_LEN__ = 999
__LED__='LED'
_ADDR = 0x5B
HOST = 'jtag.me'  # The server's hostname or IP address
PORT = 912       # Port to connect to
#i2c = busio.I2C(scl=Pin('GP1'), sda=Pin('GP0'))
#ccs811 = adafruit_ccs811.CCS811(i2c)
class CCS811:
    def __init__(self, i2c: I2C):
        self._i2c = i2c

    def setup(self):
        print("setup CCS811")
        self.multi_write_register(0xFF, b"\x11\xE5\x72\x8A")  # RESET
        time.sleep_ms(100)

        self.check_for_status_error()
        self.app_valid()

        self._i2c.writeto_mem(_ADDR, 0xF4, b"")  # APP_START
        time.sleep_ms(100)
        self.set_driver_mode(1)
        time.sleep_ms(100)

    def data_available(self) -> bool:
        v = self._i2c.readfrom_mem(_ADDR, 0x00, 1)
        if v[0] & 1:
            e = self.read_register(0xE0)
            print("error register", hex(e[0]))
        return (v[0] & 1 << 3) > 0

    def check_for_status_error(self) -> bool:
        v = self.read_register(0x00)
        return (v[0] & 1 << 0) > 0

    def app_valid(self):
        v = self.read_register(0x00)
        return (v[0] & 1 << 4) > 0

    def set_driver_mode(self, mode: int):
        v = self.read_register(0x01)  # MEAS_MODE
        v = v[0]
        v &= ~(0b00000111 << 4)  # Clear DRIVE_MODE bits
        v |= mode << 4  # Mask in mode
        self.write_register(0x01, v)

    def read_algorithm_results(self):
        v = self.multi_read_register(0x02, 4)  # ALG_RESULT_DATA
        co2 = v[0] << 8 | v[1]
        t_voc = v[2] << 8 | v[3]
        return co2, t_voc

    def write_register(self, offset: int, value: int):
        return self._i2c.writeto_mem(_ADDR, offset, bytes([value]))

    def read_register(self, offset: int):
        return self._i2c.readfrom_mem(_ADDR, offset, 1)

    def multi_write_register(self, offset: int, data: bytes):
        self._i2c.writeto_mem(_ADDR, offset, data)

    def multi_read_register(self, offset: int, length: int):
        return self._i2c.readfrom_mem(_ADDR, offset, length)

    def status(self):
        b = self._i2c.readfrom(_ADDR, 1)
        return b[0]

i2c = I2C(0, sda=Pin(8), scl=Pin(9))
ccs811 = CCS811(i2c)
ccs811.setup()
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
                    while (not nets.done()):
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

async def light(howlong):
    led = Pin(__LED__, Pin.OUT)
    await asyncio.sleep(howlong)
    led = Pin(__LED__, Pin.IN)

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
        led = Pin(__LED__, Pin.OUT)
        await asyncio.sleep(__MEAS_INTERVAL__)
        led = Pin(__LED__, Pin.IN)
        if not ccs811.data_available():
            await asyncio.sleep(__MEAS_INTERVAL__*2)
        r = c.read_algorithm_results()
        print(r)
        temp = r.temperature
        co2 = r.eco2
        tvoc = r.tvoc
        #temp_f = temp * (9/5) + 32.0
        #print(time.gmtime(0)[0])
        #yr, Month, date, h, m, s, weekday, yearday
        li_mem_clog.append([time.mktime(time.gmtime()), temp, co2, tvoc])
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

led = Pin(__LED__, Pin.OUT)
time.sleep(1)
led = Pin(__LED__, Pin.IN)
asyncio.run(main())



