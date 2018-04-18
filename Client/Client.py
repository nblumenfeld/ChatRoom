# Python program to implement client side of chat room.
import socket
import select
import sys
import json
from Tkinter import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('localhost',1134))
server.send(json.dumps({'username':'testUser'}))

## Everything below this can be commented out if you just want to test the initial connection protocol

window = Tk()
messages = Text(window)
messages.pack()
input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.pack(side=BOTTOM, fill=X)

def Enter_pressed(event):
    input_get = input_field.get()
    server.send(json.dumps({'message':input_get}))    
    input_user.set('')
    return "break"

frame = Frame(window)  # , width=300, height=300)
input_field.bind("<Return>", Enter_pressed)
frame.pack()

window.mainloop()






while True:
    sockets_list = [sys.stdin, server]

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            jsonMessage = socks.recv(2048)
            data = json.loads(jsonMessage)
            print(data["message"])
        else:
            message = sys.stdin.readline()
            server.send(json.dumps({'message':message}))
            sys.stdout.flush()

server.close()
