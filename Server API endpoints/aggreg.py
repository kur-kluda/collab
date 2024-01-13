import socket
# pip install dnspython mysql-connector-python
import dns.query
import dns.resolver
import json
import mysql
from datetime import datetime
import mysql.connector
import asyncio
import base64
dbg1=0
dbg2=0
__DEBUG_LEVEL_2_ = True if dbg2==1 else False
__DEBUG_LEVEL_1_ = True if dbg1==1 else False
__DB_SYNC_UPDATE_INTERVAL__ = 11

SENSORS_IDS_SINGLE_DIMENSIONS = [6, 11]
dns_se = '8.8.8.8'                               #
dm = 'jtag.me'
# Port to listen ond
PORT = 911 
SERV_NAME = "temp 1 aggr"

resolver = dns.resolver.Resolver()               #
resolver.nameservers = [dns_se]                  #
answer = resolver.resolve(dm, 'A')               # 
HOST = dm                                 # Konfigurē servera DNS iestatījumus,
                                                 # atrisina domēna “jtag.me” IP adresi un iestata servera resursdatoru un portu.
for r in answer: 
	HOST = r.address                                # 
	break                                        #
#HOST = socket.getaddrinfo('jtag.me', 80)[0][-1] # Izveido socket jeb ligzdu (Ligzda ir komunikācijas savienojuma beigu punkts starp programmām, kas tiek darbinātas uz tīkla)),
                                                    # saista to ar norādīto resursdatoru (host) un portu un sāk klausīties ienākošos savienojumus.
#with open('..\\serv\\db.yaml', 'r') as f:
with open('db.yaml', 'r') as f: 
   cfg = json.load(f)           
with open('db_meta.yaml', 'r') as f: 
   cfg_meta = json.load(f) 
# Create a socket object TODO: closewait??
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                                                                  #
# Bind the socket to the host and port                            #
# Izveido ligzdu, saista to ar norādīto resursdatoru un portu un sāk klausīties ienākošos savienojumus.
server_socket.bind(('', PORT))
#
# Listen for incoming connections
server_socket.listen()

print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {SERV_NAME} Server listening on {HOST.split('.')[-1]}:{PORT}")

lastInterval = 0

#TODO: lock??
async def configurator(r, client_socket, client_address, dheader):
    global lastInterval
    if(__DEBUG_LEVEL_2_):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} configurator")
    try:
        if(__DEBUG_LEVEL_2_):
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} configurator {dheader}")
        relhref = dheader.split(' ')
        if(len(relhref)<2):
            r.close()
            client_socket.close()
            return
        varname = relhref[1].split('?')
        if(len(varname)<2):
             if(relhref[1].find("favicon.ico")>-1):
                favicon_path = "favicon.ico"
                response = 'HTTP/1.1 200 OK\n'
                with open(f"{favicon_path}", "rb") as f:
                    d = f.read()
                response += f"Content-Type: image/x-icon\r\nContent-Length: {len(d)}\n\n"
                client_socket.send(response.encode())
                #response += d.decode('utf-8')
                client_socket.sendall(d)
                #client_socket.send("403 FORBIDDEN\n".encode())
             r.close()
             client_socket.close()
             return
        if not varname[1].isnumeric():
            r.close()
            client_socket.close()
            return
        pi = int(varname[1])^ord('c')
        if(pi>0):
            lastInterval=int(pi)
            if(__DEBUG_LEVEL_1_):
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} configurator: updated {str(pi)}")
        client_socket.send("200 OK\n".encode())
    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} configurator Error: {e}")
    finally:
        # Close the client socket
        if(r):
            try:
                r.close()
            finally:
                ...
        if(client_socket):
            try:
                client_socket.close()
            finally:
                ...

async def rdr(r, client_socket, client_address, dheader):
    global lastInterval
    if(__DEBUG_LEVEL_2_):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} rdr")
    try:
        client_socket.send(str(lastInterval^ord('d')).encode())
    finally:
        # Close the client socket
        if(r):
            try:
                r.close()
            finally:
                ...
        if(client_socket):
            try:
                client_socket.close()
            finally:
                ...

async def rdr_meta_out_of_memory(r, client_socket, client_address, dheader):
        db = None
        if(__DEBUG_LEVEL_2_):
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} rdr_meta_out_of")
        try:
            intt = int(dheader)#.strip(";"))
            db = mysql.connector.connect(
                port = cfg_meta["db"]["port"],
                host=cfg_meta["db"]["host"],
                user=cfg_meta["db"]["user"],
                password=cfg_meta["db"]["password"],
                database=cfg_meta["db"]["database"]
            )
            cur = db.cursor()
            sql = "SELECT `update_interval` FROM `a_hubmeta` WHERE `a_hubmeta`.`nr` = %s"
            cur.execute(sql, (intt,))
            res = cur.fetchall()
            dic = 0
            for rr in res:
                dic = rr[0]^ord('d')
            #client_socket.send((json.dumps(dic)+"\n").encode())
            client_socket.send((str(dic)+"\n").encode())
        except Exception as ex:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} rdr out of mem: {ex}")
        
        finally:
            if(db):
                try:
                    db.close()
                finally:
                    ...
            # Close the client socket
            if(r):
                try:
                    r.close()
                finally:
                    ...
            if(client_socket):
                try:
                    client_socket.close()
                finally:
                    ...

async def rdr_meta(r, client_socket, client_address, dheader):
        global SYNC_TIMES
        if(__DEBUG_LEVEL_2_):
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} rdr_meta")
        db = None
        try:
            intt = int(dheader)#.strip(";"))
            client_socket.send((str(SYNC_TIMES[intt])+"\n").encode())
        except Exception as ex:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} rdr_meta: {ex}")
        finally:
            if(db):
                try:
                    db.close()
                finally:
                    ...
            # Close the client socket
            if(r):
                try:
                    r.close()
                finally:
                    ...
            if(client_socket):
                try:
                    client_socket.close()
                finally:
                    ...
    

async def sync(r, client_socket, client_address, header):
    global SENSORS_IDS_SINGLE_DIMENSIONS
    if(__DEBUG_LEVEL_2_):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} sync fn")
    db = None
    try:
        data = json.loads(r.readline())
        metadata = json.loads(header)
        #print("{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} sync: {metadata}")
        if(metadata.get("y")):
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} yyy")
        if(__DEBUG_LEVEL_1_):
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} SYNC @ {client_address[0].split('.')[-1]} sens: {metadata['id']} d_len: {len(data)}")
        if(metadata["len"]==len(data)):
            db = mysql.connector.connect(
                host=cfg["db"]["host"],
                user=cfg["db"]["user"],
                password=cfg["db"]["password"],
                database=cfg["db"]["database"]
            )
            cur = db.cursor()
            t = datetime(1970, 1, 1, 0, 0, 0)
            epots = datetime.timestamp(t)

            date_time = datetime(int(metadata["epoch"]), 1, 1, 0, 0, 0)
            ts = datetime.timestamp(date_time)
            base_ts = ts+epots
            sql=""
            #print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} id: {metadata['id']} len: {len(metadata)} longq: {metadata['id']!=6}")
            #print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} data")
            has_more_than_one_column = metadata["id"] not in SENSORS_IDS_SINGLE_DIMENSIONS
            if(has_more_than_one_column):
                sql = "INSERT INTO `s_"+str(metadata["id"])+ "` (`time`, `rcv`, `1`, `2`) VALUES (%s, %s, %s, %s)"
            else:
                sql = "INSERT INTO `s_"+str(metadata["id"])+ "` (`time`, `rcv`, `1`) VALUES (%s, %s, %s)"
            for n in data:
                dt_object = datetime.fromtimestamp(base_ts+n[0])
                if(has_more_than_one_column):
                    val = (dt_object.strftime('%Y-%m-%d %H:%M:%S'), 
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                       float(n[1]), float(n[2]))
                else:
                    val = (dt_object.strftime('%Y-%m-%d %H:%M:%S'), 
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                       float(n[1]))
                cur.execute(sql, val)
            db.commit()
            db.close()
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} wrote {len(data)}")
            #client_socket.send((str(len(data))+" "+str((lastInterval)^ord('d'))).encode())
            client_socket.send(str(len(data)).encode())

    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Error sync: {e}")

    finally:
        if(db):
            try:
                db.close()
            finally:
                ...
        # Close the client socket
        if(r):
            try:
                r.close()
            finally:
                ...
        if(client_socket):
            try:
                client_socket.close()
            finally:
                ...

lastInterval = 0

SYNC_TIMES={}
async def sync_db():
    global SYNC_TIMES, __DB_SYNC_UPDATE_INTERVAL__
    if(__DEBUG_LEVEL_2_):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} sync_db")
    db = mysql.connector.connect(
                port = cfg_meta["db"]["port"],
                host=cfg_meta["db"]["host"],
                user=cfg_meta["db"]["user"],
                password=cfg_meta["db"]["password"],
                database=cfg_meta["db"]["database"]
            )
    cur = db.cursor()
    sql = "SELECT `a_sensormeta`.`nr`, `a_sensormeta`.`update_interval` FROM `a_sensormeta` LEFT JOIN `a_hubmeta` ON `a_sensormeta`.`hub_id` = `a_hubmeta`.`nr` WHERE `a_hubmeta`.`nr` IN (1, 2, 3, 4)"
    #cur.execute(sql, (intt,))
    cur.execute(sql)
    res = cur.fetchall()
    dic = {}
    for rr in res:
        SYNC_TIMES[rr[0]] = int(rr[1])^ord('d')
    await asyncio.sleep(__DB_SYNC_UPDATE_INTERVAL__)

            #client_socket.send((json.dumps(dic)+"\n").encode())
            #client_socket.send((json.dumps([val for key, val in sorted(dic.items())])+"\n").encode())


async def anti_broken_pipe_halt_loop():
    if(__DEBUG_LEVEL_2_):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} anti_broken)pipe")
    sync_db_task = asyncio.create_task(sync_db())
    await asyncio.sleep(0)
    while True:
        try:
            if(sync_db_task.done()): sync_db_task = asyncio.create_task(sync_db())
            client_socket, client_address = server_socket.accept()
            asyncio.create_task(loop(client_socket, client_address))
            await asyncio.sleep(0)
        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Error At ANTIBROKEPIPE main main: {e}")

async def loop(client_socket, client_address):
    if True:
        if(__DEBUG_LEVEL_2_):
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} looop")
        try:
            #with client_socket, client_socket.makefile('rb') as r:
            r = client_socket.makefile('rb')
            # Receive the heading data from the client
            header = r.readline()
            if not header: 
                try:
                    if(r):
                        r.close()
                except Exception as e:
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [nohead] Error GC-ollecting main: {e}")
                try:
                    if(client_socket):
                        client_socket.close()
                except Exception as e:
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [nohead] Error Closing cli socket main: {e}")
            dheader = header.decode()
            #print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {dheader}")
            if(dheader.startswith("GET")):
                asyncio.create_task(configurator(r, client_socket, client_address, dheader))
                await asyncio.sleep(0)
                return
            elif(dheader.startswith("NET")):
                if(len(dheader)>4):
                    if(dheader[3]=="_"):
                        #asyncio.create_task(rdr_meta(r, client_socket, client_address, dheader.split("_")[1]))
                        asyncio.create_task(rdr_meta_out_of_memory(r, client_socket, client_address, dheader.split("_")[1]))
                        await asyncio.sleep(0)
                        return
                asyncio.create_task(rdr(r, client_socket, client_address, dheader))
                await asyncio.sleep(0)
                return
            asyncio.create_task(sync(r, client_socket, client_address, header))
            await asyncio.sleep(0)
            return
        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Error main: {e}")
            try:
                if(r):
                    r.close()
            except Exception as e:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Error GC-ollecting main: {e}")
            try:
                if(client_socket):
                    client_socket.close()
            except Exception as e:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Error Closing cli socket main: {e}")
        finally:
            ...

            
            

asyncio.run(anti_broken_pipe_halt_loop())