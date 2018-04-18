/**
 *
 * Chatroom project
 * Final coding project for Networks spring 2018
 * 
 * @author Thomas Mannsverk Eliassen
 * worked with Noah Blumenfeld
 * 
 * created 11.04.2018
 * 
 */

import java.io.*;
import java.net.*;
import java.util.concurrent.*;


public class chatServer {

    public static final int DEFAULT_PORT = 1134;

    //thread pool
    private static final Executor execute = Executors.newCachedThreadPool();


    public static void main(String[] args) throws IOException {
     
        ServerSocket server = null;

        try{
            server = new ServerSocket(DEFAULT_PORT); 

            while(true){
            
                Runnable mission = new Connection(server.accept());
                execute.execute(mission);

            }

        }
        catch (IOException ioe){ System.err.println(ioe); }
        finally { if(server != null) server.close(); }

    }// end main

}//end server