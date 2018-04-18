# Python program to implement client side of chat room.
import socket
import select
import sys
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('localhost',1134))

while True:

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            jsonMessage = socks.recv(2048)
            data = json.loads(jsonMessage)
            print data["message"]
        else:
            message = sys.stdin.readline()
            server.send(json.dumps({'message':message}))
            sys.stdout.flush()

server.close()
