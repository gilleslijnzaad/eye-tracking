Eye-tracking
==================================
Code for integrating the EyeLink eye-tracker into a Java experiment.

General
----------------------------------
There are two components to the code: a Java component and a Python component. 
The Python component communicates directly with the EyeLink eye-tracker using the official PyLink module (available for download via the [SR Research Forum](https://www.sr-support.com/)).
The Java component communicates with the Python component and contains methods to include within your Java experiment. 
The two components communicate through networking, with the Java part acting as the server and the Python part as the client.

Java
----------------------------------
The server is launched by running the `main()` method of the ServerMain class. 
This creates a Server object and an Experiment object. 

The Server object first connects to the Python client. 
Then it starts a thread to continuously receive messages from the client. 
Most importantly, it contains the `send()` method that the Experiment object will use to send messages to the Python client.

The Experiment object contains a large number of methods that can be used to start processes in the eye-tracker, e.g. `prepareTrial()` or `doDriftCorrection()`. When it is created, it calls upon the actual experiment program to start.

The Demo class is meant to be a kind of pseudocode, more so than a working example. 
It demonstrate how and where to use the methods from the Experiment object.

Python
----------------------------------
The client is launched by running `main.py`. 
This sets up the connection with the eye-tracker and starts a thread to continuously receive input from the server. 
The latter is done through `client.py`.

`client.py` contains the methods to receive input from and send output to the server. 
The input that is received is then converted to an action using `input_handler.py`.

`input_handler.py` links the String input to the corresponding variable or function of `main.py`. 
For example, the message `info/ EDF P1.EDF` corresponds to changing `edf_file_name` in `main.py` to `P1.EDF`. 
The message `do/ START RECORDING` corresponds to executing `start_recording()` in `main.py`.