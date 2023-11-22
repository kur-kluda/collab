import socket
import json
# pip install dnspython mysql-connector-python
import dns.query
import dns.resolver
import json
import mysql
from datetime import datetime
import mysql.connector
# Server settings
#HOST = 'jtag.me'  # The server's hostname or IP address
dns_se = '8.8.8.8'
dm = 'jtag.me'
resolver = dns.resolver.Resolver()
resolver.nameservers = [dns_se]
answer = resolver.resolve(dm, 'A')
HOST = 'jtag.me'
for r in answer:
	HOST = r.address
	break
#HOST = socket.getaddrinfo('jtag.me', 80)[0][-1]
print(HOST.split('.')[-1])
PORT = 912      # Port to listen ond


#with open('..\\serv\\db.yaml', 'r') as f:
with open('db.yaml', 'r') as f:
   cfg = json.load(f)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Server listening on {HOST.split('.')[-1]}:{PORT}")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Connection from {client_address[0].split('.')[-1]}")

    try:
        with client_socket, client_socket.makefile('rb') as r:
        # Receive the data from the client
            header = r.readline()
            if not header: break
            data = json.loads(r.readline())
            metadata = json.loads(header)
            #print(metadata)
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
            cur = db.cursor()

            cur.execute("SELECT `1`, `2` FROM `s_1` ORDER BY rcv DESC LIMIT 1")

            result = cur.fetchall()
            
            answer = []
            answer.append(len(data))
            for x in result:
                answer.append(x)
            db.close()
            
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} wrote {len(data)}")
            client_socket.send(json.dumps(answer).encode())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the client socket
        client_socket.close()
