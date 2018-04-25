# Python program to implement client side of chat room.
import socket
import select
import sys
import json
from Tkinter import *
from threading import Thread

username = sys.argv[1]

"""handles recieving of messages"""
def receive():
    while True:
        try:
            jsonMessage = server.recv(2048)
            data = json.loads(jsonMessage)
            messages.insert(END,"%s: %s\n" % (data["sender"], data["message"]))
        except OSError:
            break

"""sends user messages to the server"""
def send(event):
    input_get = input_field.get()
    messages.insert(END, "%s: %s\n" % (username, input_get))    
    server.send(json.dumps({'message':input_get}))
    input_user.set('')
    return "break"


window = Tk()
window.title("T1P Chat Room")
frame = Frame(window)
scrollbar= Scrollbar(frame)


messages = Listbox(frame,height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
messages.pack(side=LEFT, fill=BOTH)
messages.pack()

frame.pack()

input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.pack(side=BOTTOM, fill=X)

input_field.bind("<Return>", send)
frame.pack()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('localhost',1134))
server.send(json.dumps({'username':username}))

receive_thread = Thread(target=receive)
receive_thread.start()


mainloop() # Starts the GUI execution
