#rRrrrrrrrrrrrrrrrrrrrrrr
from aiohttp import web
import aiohttp
import asyncio
import requests
#from aiojobs.aiohttp import setup, spawn


async def omgnotatask(app):
    asyncio.create_task(singletonrun())
    await asyncio.sleep(0)

async def readUntilNewLine(reader, encoding='ascii') -> str:
    #sofar =[]
    idiotpython =[]
    #~~~~~~~~~~~~ whynot_plus_0 = bytearray()
    try:
        bt=b'1'
        while bt is not None:
            bt = await reader.read(1)
            if(bt==b'\r'):
                await reader.read(1)
                if(len(idiotpython)<1):
                    return ""
                return "".join([i.decode(encoding) for i in idiotpython])# whynot_plus_0.decode(encoding)
            else:
                # apnika TypeError: 'bytes' object cannot be interpreted as an integer
                #sofar.append(bt+0)
                #~~~~~~~~~~~~ whynot_plus_0.append(bt)~
                idiotpython.append(bt)
    except Exception as ex:
        if(len(idiotpython)<1):
            return ""
        return "".join([i.decode(encoding) for i in idiotpython])# wwhynot_plus_0.decode(encoding)

async def singletonrun():
    s = 'http://c.jtag.me:81/stream'
    global sin_session
    HOST="c.jtag.me"
    PORT=81
    reader, writer = await asyncio.open_connection(HOST, PORT)
    request = f"GET /stream HTTP/1.1\r\nHost: {HOST}\r\n\r\n"
    writer.write(request.encode())
    await writer.drain()
    #headerris>>
    #hdlen = len(b'HTTP/1.1 200 OK\r\nContent-Type: multipart/x-mixed-replace;boundary=123456789000000000000987654321\r\nTransfer-Encoding: chunked\r\n')
    #response = await reader.read(hdlen)
    okstr = await readUntilNewLine(reader)
    if(okstr!="HTTP/1.1 200 OK"):
        print("TODOO: handle cant connect exception")
    okstr = await readUntilNewLine(reader)
    if(len(okstr) < len('Content-Type: ')):
        print("TODOO: handle cont type connect exception")
    #h0 = response.decode().split("\r\n")
    while len(response)>2:
        try:
            response = await reader.read(1024)
            h0 = response.decode().split("\r\n")
            response = requests.get(s, timeout=5)
            print(response.headers)
        except requests.exceptions.Timeout:
            print("The request timed out")
            await asyncio.sleep(2)
            continue
        async with sin_session.get(s) as resp:
            print(await resp.text())
            reader = aiohttp.MultipartReader.from_response(resp)
            while True:
                part = await reader.next()
                if part is None:
                    break
                print(part.headers)

async def handle(request):
   reader = await aiohttp.MultipartReader.from_response(request)
   while True:
       part = await reader.next()
       if part is None:
           break
       print(part)
   return web.Response()

"""
async def mainbody():
    #error no main run?? from asyncio...
    asyncio.create_task(singletonrun(sin_session))
    #Cannot run the event loop while another loop is running
    web.run_app(app)
    #run_app(app, host='127.0.0.1', port=2000)
"""

#scheduler = aiojobs.Scheduler()
app = web.Application()
app.router.add_route('GET', '/', handle)
sin_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=50, connect=10, sock_connect=10))
app.on_startup.append(omgnotatask)
web.run_app(app)
"""
asyncio.run(mainbody())
"""