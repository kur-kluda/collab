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
dbg1=1
dbg2=1
__DEBUG_LEVEL_2_ = True if dbg2==1 else False
__DEBUG_LEVEL_1_ = True if dbg1==1 else False

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
    try:
        if(__DEBUG_LEVEL_2_):
            print(dheader)
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
                print(f'updated {str(pi)}')
        client_socket.send("200 OK\n".encode())
    except Exception as e:
        print(f"configurator Error: {e}")
    finally:
        if(r):
            r.close()
        if(client_socket):
            client_socket.close()

async def rdr(r, client_socket, client_address, dheader):
    global lastInterval
    client_socket.send(str(lastInterval^ord('d')).encode())
    r.close()
    client_socket.close()

async def rdr_meta(r, client_socket, client_address, dheader):
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
            sql = "SELECT `a_sensormeta`.`nr`, `a_sensormeta`.`update_interval` FROM `a_sensormeta` LEFT JOIN `a_hubmeta` ON `a_sensormeta`.`hub_id` = `a_hubmeta`.`nr` WHERE `a_hubmeta`.`nr` = %s"
            cur.execute(sql, (intt,))
            res = cur.fetchall()
            dic = {}
            for r in res:
                dic[r[0]] = r[1]^ord('d')
            #client_socket.send((json.dumps(dic)+"\n").encode())
            client_socket.send((json.dumps([val for key, val in sorted(dic.items())])+"\n").encode())
            db.close()
            client_socket.close()
        except Exception as ex:
            print(ex)
            try:
                db.close()
            finally:
                ...
    

async def sync(r, client_socket, client_address, header):
    global SENSORS_IDS_SINGLE_DIMENSIONS
    try:
        db = None
        data = json.loads(r.readline())
        metadata = json.loads(header)
        #print(metadata)
        if(metadata.get("y")):
            print("yyy")
        if(__DEBUG_LEVEL_1_):
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} SYNC @ {client_address[0].split('.')[-1]} se: {metadata['id']} d: {len(data)}")
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
            #print(f"id: {metadata['id']} len: {len(metadata)} longq: {metadata['id']!=6}")
            #print(data)
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
        print(f"Error sync: {e}")

    finally:
        if(db):
            try:
                db.close()
            finally:
                just_try_no_need_for_finally_or_catch=""
        # Close the client socket
        r.close()
        client_socket.close()

lastInterval = 0
async def loop():
    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()

        try:
            #with client_socket, client_socket.makefile('rb') as r:
            r = client_socket.makefile('rb')
            # Receive the heading data from the client
            header = r.readline()
            if not header: continue
            dheader = header.decode()
            #print(dheader)
            if(dheader.startswith("GET")):
                asyncio.create_task(configurator(r, client_socket, client_address, dheader))
                await asyncio.sleep(0)
                continue
            elif(dheader.startswith("NET")):
                if(len(dheader)>4):
                    if(dheader[3]=="_"):
                        asyncio.create_task(rdr_meta(r, client_socket, client_address, dheader.split("_")[1]))
                        await asyncio.sleep(0)
                        continue
                asyncio.create_task(rdr(r, client_socket, client_address, dheader))
                await asyncio.sleep(0)
                continue
            asyncio.create_task(sync(r, client_socket, client_address, header))
            await asyncio.sleep(0)
            continue
        except Exception as e:
            print(f"Error main: {e}")
        finally:
            try:
                if(r):
                    r.close()
                if(client_socket):
                    client_socket.close()
            except Exception as e:
                print(f"Error GC-ollecting main: {e}")
            finally:
                just_try_no_need_for_finally_or_catch=""

asyncio.run(loop())