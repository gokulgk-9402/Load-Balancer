# run this code in terminal like "python client.py {client_id}" for ex: python client.py 1

import socket
import sys
import time
import os

BUFFER_SIZE = 64
FORMAT = 'utf-8'

client_id = int(sys.argv[1])

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

query = input("Enter query: ")

q = query.split()

print(f"Sending request from client {client_id}")

sock.send(query.encode(FORMAT))
start = time.time()

if q[0].lower() == "file":
    print(f'Preparing to receive the file: {q[-1]}')
    filesize = sock.recv(BUFFER_SIZE).decode(FORMAT)
    # print(filesize)

    if filesize == "File not found":
        print(f"File {q[-1]} not found in server!")

    else:

        filename = os.path.basename(q[-1])
        filesize = int(filesize)

        with open(filename, "wb") as f:
            bytes_read = sock.recv(filesize)
            f.write(bytes_read)

        print(f"File {q[-1]} received successfully!")

else:
    msg = sock.recv(1024).decode(FORMAT)

    print(msg)

end = time.time()

print(f"Time taken: {end - start}")