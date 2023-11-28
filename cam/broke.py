#rRrrrrrrrrrrrrrrrrrrrrrr
from aiohttp import web
import aiohttp
import asyncio
import requests
#from aiojobs.aiohttp import setup, spawn


async def omgnotatask(app):
    asyncio.create_task(singletonrun())
    await asyncio.sleep(0)

async def singletonrun():
    s = 'http://c.jtag.me:81/stream'
    global sin_session

    while True:
        try:
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