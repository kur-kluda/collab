#rRrrrrrrrrrrrrrrrrrrrrrr
from aiohttp import web
from aiohttp import MultipartWriter
import aiohttp
import asyncio
import requests
import broke_utils as bu
from datetime import datetime
#from aiojobs.aiohttp import setup, spawn

__LAST_UPDATE__ = datetime.now()
__LIBRARY_SIZE__ = 120
__LIBRARY_THREAD_SAFE__ = []

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

    
    #for tt in range (123):
    while True:
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
            for oo in range(4):
                if(okstr==''):
                    okstr = await bu.readUntilNewLine(reader) 
                elif(len(okstr)<5):
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
        byarr = bytearray()
        if(clen>0):
            response = await reader.read(clen)
            byarr = await bu.appendUntilSeperator(reader, '\r\n\r\n--'+seper, response)
            """
            f = open(f"00{tt}.jpg", "bw")
            f.write(byarr)
            f.close()
            f = open(f"00{tt}noarr.jpg", "bw")
            f.write(response)
            f.close()
            """
        else:
            response = await reader.read(1024)
            byarr = bytearray(response)
        
        del response
        if(len(__LIBRARY_THREAD_SAFE__)< __LIBRARY_SIZE__):
            __LIBRARY_THREAD_SAFE__.append(byarr)
        else:
            __LIBRARY_THREAD_SAFE__.pop(0)
            __LIBRARY_THREAD_SAFE__.append(byarr)
        __LAST_UPDATE__ = datetime.now()
        await asyncio.sleep(0)

async def handle(request):
    my_boundary = "123456789000000000000987654321"
    response = web.StreamResponse(
    status=200,
    reason='OK',
    headers={
        'Content-Type': 'multipart/x-mixed-replace;boundary={}'.format(my_boundary)
    }
    )
    await response.prepare(request)
    pointer = 0
    while True:
        if(len(__LIBRARY_THREAD_SAFE__)<1):
            await asyncio.sleep(1)
            continue
        frame = __LIBRARY_THREAD_SAFE__[pointer]
        with MultipartWriter('image/jpeg', boundary=my_boundary) as mpwriter:
            mpwriter.append(frame, {
            'Content-Type': 'image/jpeg'
            })
            await mpwriter.write(response, close_boundary=False)
        await response.drain()
        pointer = pointer+1
        if(pointer>=len(__LIBRARY_THREAD_SAFE__)):
            pointer = 0

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