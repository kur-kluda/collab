#rRrrrrrrrrrrrrrrrrrrrrrr
from aiohttp import web
import aiohttp
import asyncio
import requests
import broke_utils as bu
#from aiojobs.aiohttp import setup, spawn


async def omgnotatask(app):
    asyncio.create_task(singletonrun())
    await asyncio.sleep(0)

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
    okstr = await bu.readUntilNewLine(reader)
    if(okstr!="HTTP/1.1 200 OK"):
        print("TODOO: handle cant connect exception")
    okstr = await bu.readUntilNewLine(reader)
    if(len(okstr) < len('Content-Type: ')):
        print("TODOO: handle cont type connect exception")
    if(not okstr.startswith("Content-Type")):
        print("TODOO: handle cont type not here exception")
    seper = okstr.split("=")[1]

    more_headers = [
        "Transfer-Encoding",
        "Access-Control-Allow-Origin",
        "X-Framerate"
    ]
    for h in more_headers:
        okstr = await bu.readUntilNewLine(reader)  
        if(not okstr.startswith(h)):
            print(f"TODOO: handle {h} not here exception")
    okstr = await bu.readUntilNewLine(reader)  
    if(okstr==''):
        okstr = await bu.readUntilNewLine(reader)  
    try:
        if(int(okstr)<0):
            print(f"TODOO: no integer before seperator exception")
    except Exception as e:
        print(f"TODOO: no integer before sepperator true exception")
    okstr = await bu.readUntilSeperator(reader, seper) 
    okstr = await bu.readUntilNewLine(reader) 
    if(okstr==''):
        okstr = await bu.readUntilNewLine(reader)  
        if(okstr==''):
            okstr = await bu.readUntilNewLine(reader) 

    
    for tt in range (4):
        #who is this \r\n\r\n 4e \r\n?
        #okstr = await bu.readUntilNewLine(reader) 
        # the more the headers
        more_headers = [
            "Content-Type",
            "Content-Length",
            "X-Timestamp"
        ]
        clen=0
        tmestamp=0.0
        for h in more_headers:
            for oo in range(3):
                if(okstr==''):
                    okstr = await bu.readUntilNewLine(reader) 
            okstr = await bu.readUntilNewLine(reader)  
            if(not okstr.startswith(h)):
                print(f"TODOO: handle {h} not here exception")
            if(okstr.startswith("Content-Length")):
                clen = int(okstr.split(":")[1].strip())
            elif(okstr.startswith("X-Timestamp")):
                tmestamp = float(okstr.split(":")[1].strip())
        okstr = await bu.readUntilNewLine(reader) 
        if(okstr==''):
            okstr = await bu.readUntilNewLine(reader) 
            if(okstr==''):
                okstr = await bu.readUntilNewLine(reader) 
        #who is this \r\n 39a9 \r\n ??? changes to d2de etc?? checksum??
        #okstr = await bu.readUntilNewLine(reader)          
        #h0 = response.decode().split("\r\n")
        if(clen>0):
            response = await reader.read(clen)
            byarr = await bu.appendUntilSeperator(reader, '\r\n\r\n--'+seper, response)
            f = open(f"00{tt}.jpg", "bw")
            f.write(byarr)
            f.close()
            f = open(f"00{tt}noarr.jpg", "bw")
            f.write(response)
            f.close()
        else:
            response = await reader.read(1024)

        okstr = await bu.readUntilNewLine(reader) 
        if(okstr==''):
            okstr = await bu.readUntilNewLine(reader) 
            if(okstr==''):
                okstr = await bu.readUntilNewLine(reader) 
        #who is this \r\n 39a9 \r\n ??? changes to d2de etc?? checksum??

    okstr = await bu.readUntilNewLine(reader) 
    while len(response)>2:
        try:
            h0 = response.decode().split("\r\n")
            response = await reader.read(1024)
        except requests.exceptions.Timeout:
            print("The request timed out")
            await asyncio.sleep(2)
            continue

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