#rRrrrrrrrrrrrrrrrrrrrrrr
from aiohttp import web
from aiohttp import MultipartWriter
import aiohttp
import asyncio
import requests
import sys
if(sys.platform.startswith('win')):
    import broke_utils as bu
else:
    import broke_utils_linux as bu
from datetime import datetime
#from aiojobs.aiohttp import setup, spawn

__LAST_UPDATE__ = datetime.now()
__LIBRARY_SIZE__ = 120
__LIBRARY_THREAD_SAFE__ = []
__LIBRARY_STAMPS_THREAD_SAFE__ = []
__CFG_FLUSH_ALL_WHEN_LIB_FULL__ = True
__DBGMSG__ = False
__DBG_SAVE_IMAGES__ = False
runtask = None

async def omgnotatask(app=None):
    global runtask
    runtask = asyncio.create_task(singletonrun())
    await asyncio.sleep(0)

async def singletonrun():
    #s = 'http://c.jtag.me:81/stream'
    HOST="jtag.me"
    PORT=1075
    reader, writer = await asyncio.open_connection(HOST, PORT)
    if(sys.platform.startswith('win')):
        request = f"GET /stream HTTP/1.1\r\nHost: {HOST}\r\n\r\n"
    else:
        request = f"GET /stream HTTP/1.1\nHost: {HOST}\n\n"
    writer.write(request.encode())
    await writer.drain()
    #headerris>>
    #hdlen = len(b'HTTP/1.1 200 OK\r\nContent-Type: multipart/x-mixed-replace;boundary=123456789000000000000987654321\r\nTransfer-Encoding: chunked\r\n')
    #response = await reader.read(hdlen)
    okstr = await bu.readUntilNewLine(reader)
    if(not sys.platform.startswith('win')):  
        okstr = okstr.strip()
    if(okstr!="HTTP/1.1 200 OK"):
        print(":".join("{:02x}".format(ord(c)) for c in okstr))
        #print(hex(okstr))
        print(":".join("{:02x}".format(ord(c)) for c in "HTTP/1.1 200 OK"))
        #print(hex("HTTP/1.1 200 OK"))
        print("HTTP/1.1 200 OK")
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
    if(not sys.platform.startswith('win')):    
        okstr = await reader.read(1)
        okstr = await bu.readUntilNewLine(reader)  
    try:
        if(int(okstr)<0):
            print(f"TODOO: no integer before seperator exception")
    except Exception as e:
        print(f"TODOO: no integer before sepperator true exception")
        print(e)
    okstr = await bu.readUntilSeperator(reader, seper) 
    okstr = await bu.readUntilNewLine(reader) 
    if(okstr.strip()==''):
        okstr = await bu.readUntilNewLine(reader)  
        if(okstr.strip()==''):
            okstr = await bu.readUntilNewLine(reader) 
    
    if(__DBGMSG__):
        print(f"line#87: {okstr}")    
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
            for oo in range(8):
                if(okstr.strip()==''):
                    okstr = await bu.readUntilNewLine(reader) 
                elif(len(okstr.strip())<5):
                    okstr = await bu.readUntilNewLine(reader)
                elif(okstr.strip()!=''):
                    break 
            if(not okstr.startswith(h)):
                print(f"TODOO: handle {h} not here exception")
            if(okstr.startswith("Content-Length")):
                clen = int(okstr.split(":")[1].strip())
            elif(okstr.startswith("X-Timestamp")):
                tmestamp = float(okstr.split(":")[1].strip())
            okstr = await bu.readUntilNewLine(reader) 
        if(okstr.strip()==''):
            okstr = await bu.readUntilNewLine(reader) 
            if(okstr.strip()==''):
                okstr = await bu.readUntilNewLine(reader) 
        if(__DBGMSG__):
            print(f"line#118: {okstr}")    
        #who is this \r\n 39a9 \r\n ??? changes to d2de etc?? checksum??
        #okstr = await bu.readUntilNewLine(reader)          
        #h0 = response.decode().split("\r\n")
        byarr = bytearray()
        if(__DBGMSG__):
            print(f"line#126: clen is {clen}")
        if(clen>0):
            response = await reader.read(clen)
            if(sys.platform.startswith('win')):
                byarr = await bu.appendUntilSeperator(reader, '\r\n\r\n--'+seper, response)
            else:
                byarr = await bu.appendUntilSeperator(reader, '\r\n\r\n--'+seper, response)
            if(__DBG_SAVE_IMAGES__):
                f = open(f"00{clen}.jpg", "bw")
                f.write(byarr)
                f.close()
            """
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
            __LIBRARY_STAMPS_THREAD_SAFE__.append(tmestamp)
        else:
            if(__CFG_FLUSH_ALL_WHEN_LIB_FULL__):
                if(__DBGMSG__):
                    print(f"len bef stamps {len(__LIBRARY_STAMPS_THREAD_SAFE__)}")
                for i in range(len(__LIBRARY_THREAD_SAFE__)):
                    if(i>0):
                        __LIBRARY_THREAD_SAFE__.pop(0)
                        __LIBRARY_STAMPS_THREAD_SAFE__.pop(0)
                        #del __LIBRARY_THREAD_SAFE__[i]
                        #del __LIBRARY_STAMPS_THREAD_SAFE__[i]
                if(__DBGMSG__):
                    print(f"len now stamps {len(__LIBRARY_STAMPS_THREAD_SAFE__)}")
                    print(f"len now librar {len(__LIBRARY_THREAD_SAFE__)}")
            else:
                __LIBRARY_THREAD_SAFE__.pop(0)
                __LIBRARY_STAMPS_THREAD_SAFE__.pop(0)
            __LIBRARY_THREAD_SAFE__.append(byarr)
            __LIBRARY_STAMPS_THREAD_SAFE__.append(tmestamp)
        __LAST_UPDATE__ = datetime.now()
        #await asyncio.sleep(0)

async def handle(request):
    my_boundary = "123456789000000000000987654321"
    print(f"deb {request.remote}")
    response = web.StreamResponse(
    status=200,
    reason='OK',
    headers={
        'Content-Type': 'multipart/x-mixed-replace;boundary={}'.format(my_boundary),
        "X-Framerate": "60"
    }
    )
    await response.prepare(request)
    pointer = 0
    while True:
        if(len(__LIBRARY_THREAD_SAFE__)<1):
            await asyncio.sleep(1)
            continue
        if(pointer>=len(__LIBRARY_THREAD_SAFE__)):
            pointer = 0
        frame = __LIBRARY_THREAD_SAFE__[pointer]
        with MultipartWriter('image/jpeg', boundary=my_boundary) as mpwriter:
            mpwriter.append(frame, {
            'Content-Type': 'image/jpeg',
            "X-Timestamp": str(__LIBRARY_STAMPS_THREAD_SAFE__[pointer])
            })
            await mpwriter.write(response, close_boundary=False)
        #if(not sys.platform.startswith('win')):
        #    await response.drain()
        #drain already inside write?? always?? examples enlisted drain too, no?
        #await response.write()
        pointer = pointer+1
        if(pointer>=len(__LIBRARY_THREAD_SAFE__)):
            pointer = 0
        #why linux needs this? ubuntu.. otherwise it just hangs not displaying even the first frame image..
        if(not sys.platform.startswith('win')):
#still freezes. :(            
#await asyncio.sleep(0)
            await asyncio.sleep(0.01)

async def handle_ctrl(request):
    global runtask
    if('a' in request.query):
        if(request.query['a']):
            if(request.query['a'] in ["1", "0"]):
                if(request.query['a']=="1"):
                    if(runtask):
                        runtask.cancel()
                    runtask = await omgnotatask()
                else:
                    if(runtask):
                        runtask.cancel()
                        runtask = None
                return web.Response(text=f"Done, {request.query['a']}")
    return web.Response(text=f"not ok.")



#scheduler = aiojobs.Scheduler()
app = web.Application()
app.router.add_route('GET', '/', handle)
app.router.add_route('GET', '/c', handle_ctrl)
app.on_startup.append(omgnotatask)
web.run_app(app, host='0.0.0.0', port=81)
"""
asyncio.run(mainbody())
"""
