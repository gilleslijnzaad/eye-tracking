/**
 * Server for the Java component containing methods for connecting to and 
 * communicating with the Python component.
 *
 * @author  Gilles Lijnzaad
 * @version 1.0
 * date:    June 21st, 2021
 */

import java.io.*;
import java.net.*;

public class Server {
  private final int PORT = 9000; // can be any port number as long as it is the same in client.py
  private boolean running = false;
  private ServerSocket server;
  private Socket client;

  /**
   * Creates server object by launching a ServerSocket and calling the
   * connectToClient() method.
   * @throws IOException  in case something goes wrong while launching a ServerSocket
   */
  public Server() throws IOException {
    server = new ServerSocket(PORT);
    System.out.println("Launched server");
    running = true;
    connectToClient();
  }
  
  /**
   * Connects to the Python client and then starts a thread which continuously
   * listens to input from the client.
   */
  private void connectToClient() {
    try {
      client = server.accept();
      System.out.println("Accepted client");
    } catch (IOException e) {
      System.err.println("Something went wrong in accepting the client.");
      e.printStackTrace();
    }

    Thread t = new Thread(() -> {
      try {
        BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
        String input = in.readLine();       // stalls if there is no input
        while (running) {
          handleInput(input);
          input = in.readLine();
        }
      } catch (IOException e) {
        System.err.println("Something went wrong in receiving input from the client.");
        e.printStackTrace();
      }
    });
    t.start();
  }

  /**
   * Determines what to do with certain inputs from the client. The
   * client can send error codes from the eye-tracker, and they should  
   * be handled using this method.
   * @param input     a String received from the client
   */
  private void handleInput(String input) {
    // dummy method
  }

  /**
   * Sends output to the Python client. This method is used often 
   * in the Experiment class.
   * @param message   a String to be sent to the client
   */
  public void send(String message) {
    try {
      PrintWriter out = new PrintWriter(client.getOutputStream(), true);
      out.println(message);
    } catch (IOException e){
      System.err.println("Something went wrong in sending output to the client.");
      e.printStackTrace();
    }
  }
}
