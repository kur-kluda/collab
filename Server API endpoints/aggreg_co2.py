import socket
import json
# pip install dnspython mysql-connector-python
import dns.query
import dns.resolver
import json
import mysql
from datetime import datetime
import mysql.connector
import asyncio

dbg1=1
dbg2=0
__DEBUG_LEVEL_2_ = True if dbg2==1 else False
__DEBUG_LEVEL_1_ = True if dbg1==1 else False

# Server settings
dns_se = '8.8.8.8'
dm = 'jtag.me'
PORT = 912      # Port to listen ond
SERV_NAME = "gas 2 aggr"

resolver = dns.resolver.Resolver()
resolver.nameservers = [dns_se]
answer = resolver.resolve(dm, 'A')
HOST = dm
for r in answer:
	HOST = r.address
	break
#HOST = socket.getaddrinfo('jtag.me', 80)[0][-1]

#with open('..\\serv\\db.yaml', 'r') as f:
with open('db.yaml', 'r') as f:
   cfg = json.load(f)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
#oh no resolve takes 127anyways unless diff serverf
HOST=''
# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

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
                client_socket.sendall(d)
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

async def sync(r, client_socket, client_address, metadata, data):
    try:
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

        sql = "INSERT INTO `s_"+str(metadata["id"])+ "` (`time`, `rcv`, `1`, `2`) VALUES (%s, %s, %s, %s)"
        for n in data:
            dt_object = datetime.fromtimestamp(base_ts+n[0])
            val = (dt_object.strftime('%Y-%m-%d %H:%M:%S'), 
                   datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                   float(n[1]), float(n[2]))
            cur.execute(sql, val)
        db.commit()

        db.close()

        if(__DEBUG_LEVEL_1_):    
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} wrote {len(data)}")
        client_socket.send(str(len(data)).encode())

    except Exception as e:
        print(f"Error sync: {e}")

    finally:
        # Close the client socket
        if(r):
            r.close()
        if(client_socket):
            client_socket.close()

async def fback(r, client_socket, client_address):
    try:
        db = mysql.connector.connect(
                    host=cfg["db"]["host"],
                    user=cfg["db"]["user"],
                    password=cfg["db"]["password"],
                    database=cfg["db"]["database"]
                )
        cur = db.cursor()
        cur.execute("SELECT `1`, `2` FROM `s_1` ORDER BY rcv DESC LIMIT 1")

        result = cur.fetchall()
            
        answer = []
        for x in result:
            answer.append(x)
        db.close()
        client_socket.send(json.dumps(answer).encode())

        if(__DEBUG_LEVEL_1_):    
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} sync")

    except Exception as e:
        print(f"Error sync: {e}")

    finally:
        # Close the client socket
        if(r):
            r.close()
        if(client_socket):
            client_socket.close()           

async def loop():
    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        if(__DEBUG_LEVEL_1_): 
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Connection from {client_address[0].split('.')[-1]}")

        try:
            with client_socket, client_socket.makefile('rb') as r:
            # Receive the data from the client
                header = r.readline()
                if not header: break
                dheader = header.decode()
                if(dheader.startswith("GET")):
                    asyncio.create_task(configurator(r, client_socket, client_address, dheader))
                    await asyncio.sleep(0)
                    continue
                elif(dheader.startswith("NET")):
                    asyncio.create_task(rdr(r, client_socket, client_address, dheader))
                    await asyncio.sleep(0)
                    continue
                metadata = json.loads(header)
                #print(metadata)
                if(metadata["len"]=="MAKROK"):
                    asyncio.create_task(fback(r, client_socket, client_address))
                    await asyncio.sleep(0)
                    continue
                data = json.loads(r.readline())
                if(metadata["len"]==len(data)):
                    asyncio.create_task(sync(r, client_socket, client_address, metadata, data))
                    await asyncio.sleep(0)
                    continue
        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close the client socket
            if(r):
                r.close()
            if(client_socket):
                client_socket.close()

asyncio.run(loop())