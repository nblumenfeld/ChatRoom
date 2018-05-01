# ChatRoom
@ Author: 
    Noah Blumenfeld
    Thomas M. Eliassen 

Class project for creating a chat room based on custom protocols

For out implementation of the server and client we decided that we dont care about a max number of Clients connected
and we dont care about notifying to much if an error code is received.

Both the Server and Client are implemented using Python.
Python version 2.7

Private Messaging has been implemented

Server:
    Run the server from the command line using python:
        ```
        python chatServer.py
        ```

    The Server has 4 methods.
        def chat_server():
            #   runs the server, looks for incoming connections and messages

        def privateMessage(server_socet, sock, sender, message, dm):
            #   sends the message only to the user with a username that matches the dm field

            server_socet is the Server itself
            sock is the client sending the message
            sender is the username of the sender
            message is the message itself
            dm is the username of the targeted person for the private message


        def broadcast(server_socet, sock, sender, message):      
            #   sends the message to all users connected

            server_socet is the Server itself
            sock is the client sending the message
            sender is the username of the sender
            message is the message itself            


        def slettTing(socket):                                   
            #   method for deleting a socket connection

            socket is the socketconnection we are deleting

    In addition to these 4 methods there is a main method that starts the chat_server()
    The server starts on a defined port (1134) then runs a constant while loop loking for data sent to the server. If a new socket is detected, we add that socket to SOCKET_LIST and create a tuple with the socket and a None value that is added to connectedUsers.
    Then when the new user sends its username we find the connection in the connnectedUsers, delete the instance and read the tuple now with the username, then broadcasts a message saying the user has connected.
    
    If the server detects that there is message being sent it starts the parsing to make sure it is following protocol. If there is a disconnect key then the server responds with its own disconnect before kicking the socket and user out.

    If there is a message instead then the server checks for a dm key, if there is a name in the dm field then we start the privateMessage function. However, if the dm field is None then we start the broadcast function.

    Both the broadcast and the privateMessage loops through the list of connections. Where the broadcast function sends the message to every connected users except the server and the sender, the privateMessage only sends it to the connection that matches the dm.


Client:
    Run the client from the command line using python with username as first and only argument:
        ```
        python Client.py <Username>
        ```
    
    The client is using a Tkinter python Graphical User Interface
     
    The Client has 3 methods.
        def receive():
            #   continuously run the receiver thread looking for incoming messages.

        
        def send(event)
            #   binds the input to a message and send it to the server

            event is the bind mechanic for the GUI

        
        def disconnect():
            #   method for sending the disconnect key

    
    The client runs from a mainloop() that starts the GUI
    When starting the client from command line it takes the users Username as first argument. Then it sends the username to the server and awaits the response.
    If the server response with isConnected == True then the client has been accepted to the chat.

    From this point the receive() thread will parse through incoming messages and print them to the screen. If the dm field has the users username then it threats the incoming message as a private message. If the field is empty then it prints it as a regular message. If it receive the disconnect key then it closes the window.

    The send() thread react if the users hits enter or clicks the disconnect button. If the user clicks the disconnect button the client automatically sends the disconnect key message. 

