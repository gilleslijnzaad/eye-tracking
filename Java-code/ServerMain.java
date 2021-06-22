/**
 * This class starts up the Java server by creating a Server object.
 * Change the participant number here before every experiment, because 
 * otherwise previous eye-tracking data may be overwritten. 
 *
 * @author  Gilles Lijnzaad
 * @version 1.0
 * date:    June 21st, 2021
 */

import java.io.IOException;

public class ServerMain {
  /* These variables are all static so they can be easily accessed from other classes. */
  public static Server server;
  public static Experiment experiment;
  public static int participantNumber;

  /**
   * The main method for the Java server. Creates the Server object
   * and the Experiment object.
   * @param args    command line arguments
   */
  public static void main(String[] args) {
    try {
        server = new Server();
    } catch (IOException e) {
        System.err.println("Something went wrong when creating a server.");
        e.printStackTrace();
    }
    participantNumber = 1;
    experiment = new Experiment(participantNumber);
  }
}