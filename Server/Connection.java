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
			InputStream is = null;
			OutputStream os = null;

			InetAddress host;

			try{

				is = new BufferedInputStream(client.getInputStream());
				os = new BufferedOutputStream(client.getOutputStream());
				int numBytes = is.read(buffer);
				
				while (numBytes != -1){
					String user = new String(buffer).trim();
					try{
						host =  InetAddress.getByName(user);
						String hostString = host.getHostAddress() + "\n";
						os.write(hostString.getBytes());
						os.flush();
						is.close();

					}
					catch(UnknownHostException uhe){
						String feil = "Unknown host: " + user + "\n";
						os.write(feil.getBytes());
						os.flush();
						is.close();
					}
					finally {
						// close streams and socket
						if (is != null)
							is.close();
						if (os != null)
							os.close();
					}
				}

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
