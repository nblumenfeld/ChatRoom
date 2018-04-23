import sys
import socket
import select
import json
import datetime

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 1134
# a list of tuples with socetfd and username
connectedUser = []
maxUsers = 10

def chat_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST,[],[],0)


        for sock in ready_to_read:

            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                connectedUser.append((sock,None))

                # >> This is only server side
                # print "Client (%s, %s) connected" % addr
                
                # >> This brodcasts to everyone connected that a new connection enterd the room
                # broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
             

            # a message from a client, not a new connection
            else:

                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # there is something in the socket
                        # Data is a json object

                        data = json.loads(data)

                        print data["message"] 

                        # if socekt is in the connectedUser but with (sock, None) then we add the username
                        # look through the json object to figure out if it is a message or a connection.
                        if("username" in data):
                            connectedUser.append((sock,data["username"]))
                            sock.send(json.dumps({"isConnected":True}))
                            broadcast(server_socket,sock,data["sender"],"User has connected")
                        elif("disconect" in data):
                            if data["disconnect"] == True:
                                sock.send(json.dumps({"isConnected":True}))
                                # remove from usernameList
                                if sock in connectedUser[0]:
                                    remObject = [i for i in connectedUser if i[0] == sock]
                                    remObject = remObject[0]
                                    connectedUser.remove(remObject)
                                sock.close()
                        else:
                            melding = data["message"]
                            dm = data["dm"]
                            sender = data["sender"]

                            if dm == None:
                                broadcast(server_socket,sock,sender,melding)
                            else:
                                privatMessage(server_socket,sock,sender,melding,dm)
                                

                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        if sock in connectedUser[0]:
                                    remObject = [i for i in connectedUser if i[0] == sock]
                                    remObject = remObject[0]
                                    connectedUser.remove(remObject)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket,sock,None,"Client (%s, %s) is offline\n" % addr) 

                # exception 
                except:
                    
                    broadcast(server_socket, sock, None,"Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()

def privatMessage (server_socket, sock, sender, message, dmUser):
    if dmUser in connectedUser[0]:
        dmSocket = [i for i in connectedUser if i[0] == dmUser]
        dmSocket = dmSocket[0]
        dmSocket = dmSocket[0] #getting the socket

        now =  datetime.datetime.now()
        
        for socket in SOCKET_LIST:
            # send the message only to peer
            if socket == dmSocket:
                try :
                    socket.send(json.dumps({"dm":dmUser, "sender":sender, "message":message, "length":len(message), "date":str(now)}))
                except :
                    # broken socket connection
                    socket.close()
                    # broken socket, remove it
                    if socket in SOCKET_LIST:
                        SOCKET_LIST.remove(socket)  
                    # remove from usernameList
                    if socket in connectedUser[0]:
                        remObject = [i for i in connectedUser if i[0] == socket]
                        remObject = remObject[0]
                        connectedUser.remove(remObject)
                    

# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, sender, message):
    
    now =  datetime.datetime.now()

    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(json.dumps({"dm":None,"sender":sender, "message":message, "length":len(message), "date":str(now)}))
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
                # remove from usernameList
                if socket in connectedUser[0]:
                    remObject = [i for i in connectedUser if i[0] == socket]
                    remObject = remObject[0]
                    connectedUser.remove(remObject)
 
if __name__ == "__main__":
    #maxNum = sys.argv[1]
    sys.exit(chat_server()) 