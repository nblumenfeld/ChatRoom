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

# a error code list
errors = [1, 2]
# 1 is for username exist alread
# 2 is for IF the server have a maxnumber of users


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
                # add the user to connectedUser but with no username
                
                connectedUser.append((sockfd,None))
                print "The list after newest connection"
                print connectedUser

                print "This is the socet that connected: %s" %sockfd

            # a message from a client, not a new connection
            else:
                # process data recieved from client 
                try:
                    data = sock.recv(RECV_BUFFER)
                    
                    if data:
                        # there is something in the socket
                        # Data is a json object

                        data = json.loads(data)
                        
                        # if socekt is in the connectedUser but with (sock, None) then we check if there is a user with the same name or disconect them
                        
                        tempSock = sock

                        remObject = [i for i in connectedUser if i[0] == tempSock]
                        remObject = remObject[0]

                        if remObject[1] == None:
                            print "Yay"

                        if(remObject[1] == None):
                                
                            # there is no username so look for username
                            connectedUser.remove(remObject)
                            print "There was no username so we deleted the user from the list"
                            print connectedUser
                            print ""

                            #with one user connected user is now empty
                            currUsername = data["username"]
                            print "This is the new username %s" %currUsername

                            # see if there is another username in the list of usernames
                            userExist = [i for i in connectedUser if i[1] == currUsername] 
                            
                            if not userExist:
                                #there was no equel username 
                                print "There was no equal username in the list"
                                connectedUser.append((sock,currUsername))
                                print connectedUser
                                sock.send(json.dumps({"isConnected":True, "errorCode":-1}))
                                
                                print ""

                                broadcast(server_socket,sock,currUsername,"User has connected")

                            else:
                                # someone have the username already
                                # disconect them and send an error message
                                print "Someone already had the username %s" %currUsername
                                sock.send(json.dumps({"isConnected":False, "errorCode":errors[0]}))
                                
                                print connectedUser
                                
                                sock.close

                        else: 
                            # the client already in the list
                            # we are asuming wellbehave clients
                            print "The client already existed in our list with a username\n"

                            if("disconnect" in data):
                                print "We check if they are sending a disconect message\n"
                                if data["disconnect"] == True:
                                    
                                    sender = data["sender"]
                                    sock.send(json.dumps({"disconnect":True}))

                                    broadcast(server_socket,sock,sender, sender + " is offline\n")
                                    
                                    # remove from usernameList
                                    sock.close()
                                    slettTing(sock)

                            else:
                                print "Server recieved a regular message\n"
                                melding = data["message"]
                                dm = data["dm"]
                                sender = data["sender"]

                                if dm == None:
                                    print "They are trying to send a regular message\n"
                                    broadcast(server_socket,sock,sender,melding)
                                else:
                                    privatMessage(server_socket,sock,sender,melding,dm)
                                
                    else:
                        # remove the socket that's broken    
                        #slettTing(sock)
                        sock.close()
                        # at this stage, no data means probably the connection has been broken
                        print "Else problem check if else loop for if there is data"
                        #broadcast(server_socket,sock,None,"Client (%s, %s) is offline\n" % addr) 

                # exception 
                except:
                    print "Try problem, what is happening in try"
                    #broadcast(server_socket, sock, None,"Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()

def privatMessage (server_socket, sock, sender, message, dm):

    print "They are trying to send a private message to %s" %dm

    dmSocket = [i for i in connectedUser if i[1] == dm]
    if dmSocket:
        dmSocket = dmSocket[0]
        dmSocket = dmSocket[0] #getting the socket

        now =  datetime.datetime.now()
        
        for socket in SOCKET_LIST:
            # send the message only to peer
            if socket == dmSocket and socket != sock:
                try :
                    socket.send(json.dumps({"dm":dm, "sender":sender, "message":message, "length":len(message), "date":str(now)}))
                except :
                    # broken socket connection
                    socket.close()
                    # broken socket, remove it
                    slettTing (socket)
                    

# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, sender, message):

    now =  datetime.datetime.now()

    #print sock

    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                jsonThing = json.dumps({"dm":None,"sender":sender, "message":message, "length":len(message), "date":str(now)})
                
                print jsonThing
                socket.send(json.dumps({"dm":None,"sender":sender, "message":message, "length":len(message), "date":str(now)}))
              

            except :
                print "exception for brodcast"
                # broken socket connection
                socket.close()
                # broken socket, remove it
                slettTing (socket)

def slettTing (socket):
    # broken socket, remove it
    if socket in SOCKET_LIST:
        SOCKET_LIST.remove(socket)  
    # remove from usernameList
    if socket in connectedUser[0]:
        remObject = [i for i in connectedUser if i[0] == socket]
        remObject = remObject[0]
        connectedUser.remove(remObject)
        print connectedUser

if __name__ == "__main__":
 
    sys.exit(chat_server()) 