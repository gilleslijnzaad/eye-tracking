/**
 * Contains all methods needed to set up the eye-tracking experiment.
 *
 * @author  Gilles Lijnzaad
 * @version 1.0
 * date:    June 21st, 2021
 */

public class Experiment {
  Server s = ServerMain.server;
  private final int participantNumber;
  private static final short dimX = 1920;
  private static final short dimY = 1080;
  private long startTime = 0;

  /**
   * Starts experiment by calling the application main method
   * @param participantNumber
   */
  public Experiment(int participantNumber) {
    this.participantNumber = participantNumber;
    new Demo();
  }

  /**
   * Sends information about the experiment to the client, then
   * calls for the client to prepare the eye-tracking experiment.
   */
  public void prepareExperiment() {
    String edfFileName = "PART" + participantNumber + ".EDF";
    s.send("info/ EDF " + edfFileName);

    s.send("info/ DIM_X " + dimX);
    s.send("info/ DIM_Y " + dimY);

    s.send("do/ PREPARE EXPERIMENT");
  }

  /**
   * Sends information about the trial to the client, then calls
   * for the client to prepare the eye-tracking for this trial.
   * @param trialNumber   number of the trial
   * @param trialID       identifying factor about the trial (conditions, etc.)
   */
  public void prepareTrial(int trialNumber, String trialID) {
    s.send("info/ TRIAL_NUMBER " + trialNumber);
    s.send("info/ TRIAL_ID " + trialID);
    s.send("do/ PREPARE TRIAL");
  }

  /**
   * Calls for the client to do drift correction.
   */
  public void doDriftCorrection() {
    s.send("do/ DRIFT CORRECT");
  }

  /**
   * Calls for the client to start recording.
   */
  public void startRecording() {
    s.send("do/ START RECORDING");
  }

  /**
   * Sets start time to eventually calculate the synctime.
   */
  public void setStartTime(long time) {
    startTime = time;
  }

  /**
   * Sends start time to client, where the synctime is calculated upon arrival.
   */
  public void sendStartTime() {
    if (startTime != 0) {
      s.send("info/ START TIME " + startTime);
      startTime = 0;
    }
  }

  /**
   * Calls for the client to send a message to the eye-tracker.
   */
  public void sendToTracker(String message) {
    s.send("send/ " + message);
  }


  /**
   * Calls for the client to end this trial.
   */
  public void endTrial() {
    s.send("do/ END TRIAL");
  }

  /**
   * Calls for the client to end this experiment.
   */
  public void endExperiment() {
    s.send("do/ END EXPERIMENT");
  }
}