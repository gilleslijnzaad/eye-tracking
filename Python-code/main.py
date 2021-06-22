# Contains all actions that the Python component can execute on 
# behalf of the Java component.
# 
# author:   Gilles Lijnzaad
# version:  1.0
# date:     June 21st, 2021

import pylink
import client
import time

# These global variables will be changed by input_handler.py
display_x = 0
display_y = 0
edf_file_name = ""
trial_number = 0
trial_id = ""

pylink.EyeLink()                  # connect to eye-tracker
client.start_receiving_thread()   # make sure the client can receive messages

# Sends all commands and messages that are necessary before starting the
# eye-tracking experiment. Calls do_calibration() at the end.
def prepare_experiment():
	tracker = pylink.getEYELINK()
	if not tracker.isConnected():
		report_error("ABORT EXPERIMENT")

	tracker.openDataFile(edf_file_name)

	pylink.flushGetkeyQueue()
	tracker.setOfflineMode()

	tracker.sendCommand("screen_pixel_coords =  0 0 %d %d" % (display_x, display_y))
	tracker.sendMessage("DISPLAY_COORDS  0 0 %d %d" % (display_x, display_y))

	# Assumption for next lines: eye-tracker is version 6.10
	tracker.sendCommand("select_parser_configuration 0")
	tracker.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
	tracker.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET")

	link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'
	link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'
	tracker.sendCommand("link_event_filter = %s" % link_event_flags)
	tracker.sendCommand("link_sample_data = %s" % link_sample_flags)

	tracker.sendCommand("button_function 5 'accept_target_fixation'")

	tracker.sendCommand("pupil_size_diameter = YES")

	do_calibration()

# Performs calibration (doTrackerSetup).
def do_calibration():
	tracker = pylink.getEYELINK()
	if not tracker.isConnected():
		report_error("ABORT EXPERIMENT")

	pylink.openGraphics()
	pylink.setCalibrationColors((0, 0, 0), (255, 255, 255))
	pylink.setCalibrationSounds("", "", "")
	tracker.doTrackerSetup()
	pylink.closeGraphics()

# Sends all commands and messages that are necessary before starting
# a new trial, such as the TRIALID.
def prepare_trial():
	tracker = pylink.getEYELINK()
	if not tracker.isConnected():
		report_error("ABORT EXPERIMENT")

	record_message = "record_status_message 'Trial %d: %s'" % (trial_number, trial_id)
	tracker.sendCommand(record_message)
	tracker.sendMessage("TRIALID " + trial_id)
	print(record_message)

# Performs drift correction.
def drift_correction():
	tracker = pylink.getEYELINK()
	if not tracker.isConnected():
		report_error("ABORT EXPERIMENT")

	pylink.openGraphics()
	pylink.setDriftCorrectSounds("", "off", "off")
	drift_result = tracker.doDriftCorrect(int(display_x/2), int(display_y/2), 1, 1)
	pylink.closeGraphics()
	if drift_result == 27:
		drift_correction()

# Starts the recording.
def start_recording():
	tracker = pylink.getEYELINK()
	if not tracker.isConnected():
		report_error("ABORT EXPERIMENT")
                                            
	tracker.setOfflineMode()
	recording_error = tracker.startRecording(1, 1, 1, 1)
	if recording_error:             # 0 if successful, error code otherwise
		report_error("TRIAL ERROR")

	pylink.beginRealTimeMode(100)   # tells Windows to give priority to this

	if not tracker.waitForBlockStart(1000, 1, 0):
		report_error("TRIAL ERROR")

# Calculates the synctime by subtracting the start time (as sent by the
# server) from the current time. Sends synctime message.
def send_SYNCTIME(start_time):
	tracker = pylink.getEYELINK()
	if not tracker.isConnected():
		report_error("ABORT EXPERIMENT")

	current_time = int(time.time() * 1000)
	sync_time = current_time - start_time
	tracker.sendMessage(str(sync_time) + " SYNCTIME")

# Sends a message to the tracker that will be incorporated into the EDF file.
def send_tracker(message):
	tracker = pylink.getEYELINK()
	if not tracker.isConnected():
		report_error("ABORT EXPERIMENT")

	tracker.sendMessage(message)

# Stops recording for this trial.
def end_trial():
	tracker = pylink.getEYELINK()

	pylink.endRealTimeMode()
	pylink.pumpDelay(100)
	tracker.stopRecording()
	while tracker.getkey():
		pass

# Stops the experiment, closes up the EDF file.
def end_experiment():
	tracker = pylink.getEYELINK()

	if tracker is not None:
		tracker.setOfflineMode()
		pylink.msecDelay(500)

	tracker.closeDataFile()
	tracker.receiveDataFile(edf_file_name, edf_file_name)
	tracker.close()

# Reports error message to the server.
def report_error(error_message):
	client.send(error_message)