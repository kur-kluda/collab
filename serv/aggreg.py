import socket
import json
# pip install dnspython
import dns.query
import dns.resolver
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
print(HOST)
PORT = 911      # Port to listen ond


# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    try:
        with client_socket, client_socket.makefile('rb') as r:
        # Receive the data from the client
            header = r.readline()
            if not header: break
            metadata = json.loads(header)
            print(metadata)
            client_socket.send(str(len(metadata)).encode())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the client socket
        client_socket.close()
