# Python program to implement client side of chat room.
import socket
import select
import sys
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('localhost',1134))

while True:

    message = sys.stdin.readline()
    server.send(message)
    sts.stdout.flush()

server.close()
