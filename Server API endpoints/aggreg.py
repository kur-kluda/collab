import socket
# pip install dnspython mysql-connector-python
import dns.query
import dns.resolver
import json
import mysql
from datetime import datetime
import mysql.connector
# Server settings
#HOST = 'jtag.me'  # The server's hostname or IP address
dns_se = '8.8.8.8'                               #
dm = 'jtag.me'                                   #
resolver = dns.resolver.Resolver()               #
resolver.nameservers = [dns_se]                  #
answer = resolver.resolve(dm, 'A')               # 
HOST = 'jtag.me'                                 # Konfigurē servera DNS iestatījumus,
HOST = r.address                                 # atrisina domēna “jtag.me” IP adresi un iestata servera resursdatoru un portu.
for r in answer:                                 # 
	break                                        #
#HOST = socket.getaddrinfo('jtag.me', 80)[0][-1] #
print(HOST.split('.')[-1])                       #
PORT = 911      # Port to listen ond             #
                                                 

#with open('..\\serv\\db.yaml', 'r') as f:
with open('db.yaml', 'r') as f: # Izveido socket jeb ligzdu (Ligzda ir komunikācijas savienojuma beigu punkts starp programmām, kas tiek darbinātas uz tīkla)),
   cfg = json.load(f)           # saista to ar norādīto resursdatoru (host) un portu un sāk klausīties ienākošos savienojumus.

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #
                                                                  #
# Bind the socket to the host and port                            #
server_socket.bind(('', PORT))                                    # Izveido ligzdu, saista to ar norādīto resursdatoru un portu un sāk klausīties ienākošos savienojumus.
                                                                  #
# Listen for incoming connections                                 #
server_socket.listen()                                            # 

print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Server listening on {HOST.split('.')[-1]}:{PORT}")

lastInterval = 0
while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Connection from {client_address[0].split('.')[-1]}")

    try:
        with client_socket, client_socket.makefile('rb') as r:
        # Receive the data from the client
            header = r.readline()
            dheader = header.decode()
            #print(dheader)
            if(dheader.startswith("GET")):
                #print(dheader)
                relhref = dheader.split(' ')
                if(len(relhref)<2):
                    continue
                varname = relhref[1].split('?')
                if(len(varname)<2):
                     continue
                pi = int(varname[1])^ord('c')
                if(pi>0):
                    lastInterval=int(pi)
                    print(f'updated {str(pi)}')
                client_socket.send("200 OK\n".encode())
                continue
            elif(dheader.startswith("NET")):
                client_socket.send(str(lastInterval^ord('d')).encode())
                continue
            if not header: break
            data = json.loads(r.readline())
            metadata = json.loads(header)
            #print(metadata)
            if(metadata.get("y")):
                print("yyy")
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

                sql = "INSERT INTO `s_"+str(metadata["id"])+ "` (`time`, `rcv`, `1`, `2`) VALUES (%s, %s, %s, %s)"
                for n in data:
                    dt_object = datetime.fromtimestamp(base_ts+n[0])
                    val = (dt_object.strftime('%Y-%m-%d %H:%M:%S'), 
                           datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                           float(n[1]), float(n[2]))
                    cur.execute(sql, val)
            db.commit()
            db.close()
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} wrote {len(data)}")
            #client_socket.send((str(len(data))+" "+str((lastInterval)^ord('d'))).encode())
            client_socket.send(str(len(data)).encode())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the client socket
        client_socket.close()
