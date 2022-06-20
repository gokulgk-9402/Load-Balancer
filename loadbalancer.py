# just run this code normally
# save a json file "servers.json" in the same folder with contents "[]" before running any code

import socket
import threading
import json
import random

BUFFER_SIZE = 64
FORMAT = 'utf-8'

C_HOST = socket.gethostbyname(socket.gethostname())
C_PORT = 5050

servers_list = []
with open("servers.json", "r") as f:
    servers_list = json.load(f)

sockets = []
list_idle = []

print("Load blancer is starting...")

for server in servers_list:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connected to server {server['ID']}")
    sock.connect((server["SERVER"], server["PORT"]))
    sockets.append(sock)
    list_idle.append(server["ID"])

c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_sock.bind((C_HOST, C_PORT))

c_sock.listen()

number_idle = len(list_idle)

def process(client, msg):
    global number_idle
    while number_idle == 0:
        pass

    # s_id = random.choice(list_idle)
    s_id = min(list_idle)
    number_idle-=1
    print(f"Choosen server: {s_id}")
    list_idle.remove(s_id)

    q = msg.split()

    if q[0].lower() == "file":
        sockets[s_id-1].send(msg.encode(FORMAT))
        filesize = sockets[s_id-1].recv(1024)
        client.send(filesize)
        if filesize.decode(FORMAT) != "File not found":
            filesize = int(filesize.decode(FORMAT))
            bytes_recv = sockets[s_id-1].recv(filesize)
            client.send(bytes_recv)
        print(f"Sent requested file from server {s_id}!")

    else:

        sockets[s_id-1].send(msg.encode(FORMAT))
        msg = sockets[s_id-1].recv(1024)
        # msg += f" by server {s_id}".encode(FORMAT)
        print(f"Got response from server!")
        client.send(msg)
    number_idle+= 1
    list_idle.append(s_id)
    print(f"Sent response to client!")
        

def start():
    while True:
        client, address = c_sock.accept()
        print(f"Connected with {str(address)}")
        msg = client.recv(1024).decode(FORMAT)
        print(msg)
        print('calling function')
        trd = threading.Thread(target = process, args = (client, msg))
        trd.start()

start()