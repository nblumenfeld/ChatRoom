/**
 * Handler class containing the logic for echoing results back
 * to the client.
 *
 * original from
 * @author Greg Gagne
 * edited for chatServer
 * @author Thomas Mannsverk Eliassen
 */

import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.net.URL;

public class Handler
{
	public static final int BUFFER_SIZE = 2048;
	public static final int PORT = 1134;

	/**
	 * this method is invoked by a separate thread
	 */
	public void process(Socket client) throws java.io.IOException {
		byte[] buffer = new byte[BUFFER_SIZE];

		try{

				BufferedReader is = new BufferedReader(new InputStreamReader(client.getInputStream()));
				OutputStream os = new BufferedOutputStream(client.getOutputStream());

				//Set up the request, parsing:
				String innLine = is.readLine();
				String[] deler = innLine.split(" ");

				String req = "";

				URL host2 = null;
				try{
					host2 = new URL("http:/" + deler[1]);
					System.out.println("URL: \n" + host2);
				}
				catch(IOException e){
					System.err.println("Wrong url man:\n" + e);
				}

				String hostURL = host2.getHost();
				System.out.println("hostURL: \n" + hostURL);
				String hostRem = hostURL;
				String path = host2.getPath();
				System.out.println("path: \n" + path);

				if(path.length() == 0){
					//hostRem = hostRem+"/";
					req = "GET " + "/"+ " HTTP/1.1\r\n";
				}
				else{
					req = "GET " + path + " HTTP/1.1\r\n";
				}

				String beOm; //beOm == request
				String kobling; //kobling == connection


				System.out.println("at this point the req is: " + req);
				hostURL = "Host: " + hostURL + "\r\n";
				System.out.println("at this point the host is: " + hostURL);
				kobling = "Connection: close\r\n\r\n";
				System.out.println("at this point the connection is: " + kobling);


				//add it all together
				beOm = req + hostURL + kobling;
				System.out.println("at this point the request is: \n" + beOm);


				int numBytes;
				Socket socket = null;
				try{
					socket = new Socket(InetAddress.getByName(hostRem), 80);

					//second Socket
					InputStream isOrigin = new BufferedInputStream(socket.getInputStream());
					OutputStream osOrigin = new BufferedOutputStream(socket.getOutputStream());

					//request server
					osOrigin.write(beOm.getBytes());
					osOrigin.flush();

					//get response from server
					numBytes = isOrigin.read(buffer);
					while(numBytes != -1){
						os.write(buffer, 0, numBytes);
						os.flush();
					}

				}
				catch (Exception e){
					System.err.println("Failed: " + e);
				}
				finally {
					socket.close();
				}

				os.close();
				is.close();
				client.close();


		}
		catch (Exception e){
			System.err.println(e);
		}
		finally{
			client.close();
		}
	}
}
