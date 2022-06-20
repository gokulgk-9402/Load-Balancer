# run this code in terminal like "python server.py {server_id} {port_for_server} {time to process each request}" for ex: python server.py 1 5071 5
# make sure you have database credentials correct in the file "database.json"

import socket
import time
import sys
import json
import psycopg2
import os

server_id = int(sys.argv[1])

SERVER = socket.gethostbyname(socket.gethostname())
PORT = int(sys.argv[2])

p_time = int(sys.argv[3])

BUFFER_SIZE = 64
FORMAT = 'utf-8'

with open("database.json", "r") as f:
    db = json.load(f)

conn = psycopg2.connect(database = db["database"], user = db["user"], password = db["password"], host = "127.0.0.1", port = "5432")

print("Connected to databse successfully")
cur = conn.cursor()

ls = []
with open("servers.json", "r") as f:
    ls = json.load(f)

ls.append({"ID": server_id, "SERVER": SERVER, "PORT": PORT})

with open("servers.json", "w") as f:
    json.dump(ls, f)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))


def incoming(lb):
    while True:
        req=lb.recv(1024).decode(FORMAT)
        if req == "":
            continue
        print(req)
        print("Received request. Processing...")
        q = req.split()
        if q[0].lower() == "file":
            if not os.path.isfile(q[-1]):
                time.sleep(p_time)
                lb.send("File not found".encode(FORMAT))
            else:
                filesize = os.path.getsize(q[-1])
                file_len = str(filesize).encode(FORMAT)
                file_len += b' ' * (BUFFER_SIZE - len(file_len))
                # print(filesize)
                # print(file_len)
                lb.send(file_len)
                time.sleep(p_time)
                print("Starting to send file")
                with open(q[-1], "rb") as f:
                    while True:
                        bytes_read = f.read(filesize)
                        if not bytes_read:
                            break
                        lb.send(bytes_read)

                print(f"File {q[-1]} sent successfully")

        else:
            cur.execute(req)
            resp = cur.fetchall()

            response = ""
            if len(resp) == 0:
                response = "No output"
    
            for row in resp:
                response += f"Name: {row[0]} \nHEX: {row[1]} \nRGB: {row[2]}\n\n"

            time.sleep(p_time)

            lb.send(response.encode(FORMAT))
            print("Response sent!")


print(f"Server {server_id} is starting...")
server.listen()
print(f"Server is listening on {SERVER, PORT}.")
lb, address = server.accept()
print(f"Connected with {str(address)}")
print(str(lb))

incoming(lb)