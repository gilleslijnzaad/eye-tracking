# Executes functions from main.py based on the messages
# received from the Java server
# 
# author:   Gilles Lijnzaad
# version:  1.0
# date:     June 21st, 2021

import main

# Parses the first part of the message and calls
# for the next appropriate step.
def handle_input(input_string):
	if input_string.startswith("info/ "):
		information = input_string[len("info/ "):]
		set_info(information)

	elif input_string.startswith("do/ "):
		command = input_string[len("do/ "):]
		perform_action(command)

	elif input_string.startswith("send/ "):
		message = input_string[len("send/ "):]
		main.send_tracker(message)

	else:
		print("ERROR: Invalid message")

# Called for messages that started with "info/ ". 
# Changes a variable in main.py
def set_info(information):
	if information.startswith("EDF "):
		main.edf_file_name = information[len("EDF "):]
	elif information.startswith("DIM_X "):
		dimx_string = information[len("DIM_X "):]
		main.display_x = int(dimx_string)
	elif information.startswith("DIM_Y "):
		dimy_string = information[len("DIM_Y "):]
		main.display_y = int(dimy_string)
	elif information.startswith("TRIAL_NUMBER "):
		number_string = information[len("TRIAL_NUMBER "):]
		main.trial_number = int(number_string)
	elif information.startswith("TRIAL_ID "):
		main.trial_id = information[len("TRIAL_ID "):]
	elif information.startswith("START TIME "):
		time_string = information[len("START TIME "):]
		main.send_SYNCTIME(int(time_string))
	else:
		print("ERROR: Invalid info")

# Dictionary linking a message to the corresponding
# function from main.py
command_to_action = {
	"PREPARE EXPERIMENT" : main.prepare_experiment,
	"PREPARE TRIAL" : main.prepare_trial,
	"DRIFT CORRECT" : main.drift_correction,
	"START RECORDING" : main.start_recording,
	"END TRIAL" : main.end_trial,
	"END EXPERIMENT" : main.end_experiment
}

# Called for messages that start with "do/ ".
# Executes the main.py function as determined
# by the command_to_action dictonary above.
def perform_action(command):
	command_to_action[command]()