/**
 * This class shows how to use the methods from the Server class.
 * It is not meant to be runnable.
 *
 * @author  Gilles Lijnzaad
 * @version 1.0
 * date:    June 21st, 2021
 */

public class Demo {
  private int numberOfTrials = 5;
  private Experiment e = ServerMain.experiment;

  /**
   * Creates the Demo object.
   */
  public Demo() {
    e.prepareExperiment();

    for (int i = 0; i < numberOfTrials; i++) {
      String trialID = "short String identifying this trial";
      e.prepareTrial(i, trialID);
      if (i != 0) { // no drift correction right after initial calibration
        e.doDriftCorrection();
      }
      e.setStartTime(System.currentTimeMillis());
      doTrial();
    }

    e.endExperiment();
  }

  /**
   * Dummy class for the trial itself.
   */
  private void doTrial() {
    e.startRecording();
    // PAINT GRAPHICS HERE
    e.sendStartTime();
    // START ACTUAL TRIAL HERE
    e.sendToTracker("IMPORTANT INFO");
    // TRIAL STILL GOING HERE
    e.sendToTracker("OTHER INFO");
    e.endTrial();
  }
}
