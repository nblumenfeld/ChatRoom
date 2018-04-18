/**
 * This is the separate thread that services each
 * incoming echo client request.
 *
 * @author Greg Gagne
 *
 * Used for chatServer
 */

import java.net.*;
import java.io.*;
import org.json;

public class Connection implements Runnable
{
	private Socket	client;
	public static final int BUFFER_SIZE = 2048;
	
	public Connection(Socket client) {
		this.client = client;
	}

    /**
     * This method runs in a separate thread.
     */
	public void run() {
		try {

			byte[] buffer = new byte[BUFFER_SIZE];
			BufferedReader is = null;
			OutputStream os = null;

			try{

				is = new BufferedReader(new InputStream(client.getInputStream()));
				os = new BufferedOutputStream(client.getOutputStream());
				
				Strin
				
			}
			catch (Exception e){
				System.err.println(e);
			}
			finally{
				client.close();
			}			



		}
		catch (java.io.IOException ioe) {
			System.err.println(ioe);
		}
	}
}
