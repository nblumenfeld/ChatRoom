# Python program to implement client side of chat room.
import socket
import select
import sys
import json
from Tkinter import *
from threading import Thread

username = sys.argv[1]
dm = None

"""handles recieving of messages in its own thread"""
def receive():
    isConnected = False
    while True:
        if(isConnected == False):
            while not isConnected:
                try:
                    jsonMessage = server.recv(2048)
                    data = json.loads(jsonMessage)
                    if(data["isConnected"] == True):
                        isConnected = True
                    else if(data['errorCode'] == 1):
                        messages.insert(END, 'Username taken')
                        window.destroy()
                    else if(data['errorCode'] == 2):
                        messages.insert(END, 'Too many kooks')
                        window.destroy()
                except OSError:
                    break
        else:
            while True:
                try:
                    jsonMessage = server.recv(2048)
                    data = json.loads(jsonMessage)
                    if('disconnect' in data):
                        window.destroy()
                    if('dm' in data):
                        if(data['dm'] == username):
                            messages.insert(END, 'DIRECT MESSAGE!!! %s: %s' %(data["sender"], data["message"]))
                    else:
                        messages.insert(END,"%s: %s\n" % (data["sender"], data["message"]))
                except OSError:
                    break


"""sends user messages to the server"""
def send(event):
    input_get = input_field.get()
    dm = inputDM.get()
    messages.insert(END, "You: %s\n" %  input_get)   
    messageToSend = json.dumps({'message':input_get}) 
    if dm == '':
        print 'Sending without DM'
        server.send(json.dumps({'message':input_get, 'sender':username, 'dm':None}))
    else:
        server.send(json.dumps({'message':input_get, 'sender':username, 'dm':dm}))
    input_user.set('')
    return "break"

def disconnect():
    server.send(json.dumps({'disconnect':True,'sender':username}))


window = Tk()
window.title("T1P Chat Room")
frame = Frame(window)
scrollbar= Scrollbar(frame)


messages = Listbox(frame,height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
messages.pack(side=LEFT, fill=BOTH)
messages.pack()

frame.pack()

labelDMText=StringVar()
labelDMText.set("DM:")
labelDM = Label(window, textvariable=labelDMText)
inputDM = StringVar()
inputDMField = Entry(window, textvariable=inputDM)
labelDM.pack(side=LEFT)
inputDMField.pack(side=LEFT)

messageLabelText = StringVar()
messageLabelText.set("Message:")
messageLabel = Label(window, textvariable=messageLabelText)
input_user = StringVar()
input_field = Entry(window, textvariable=input_user)
messageLabel.pack(side=LEFT)
input_field.pack(side=LEFT)

input_field.bind("<Return>", send)

disconnectButton = Button(window, text="Disconnect", command=disconnect)
disconnectButton.pack(side=BOTTOM)
frame.pack()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('146.86.79.208',1134))
print server

receive_thread = Thread(target=receive)
receive_thread.start()

# server.connect(('localhost',1134))
server.send(json.dumps({'username':username}))




mainloop() # Starts the GUI execution
