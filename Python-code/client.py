# Contains functions that are used to establish communication between the
# Java server and the Python client.
# 
# author:   Gilles Lijnzaad
# version:  1.0
# date:     June 21st, 2021

import socket
import threading

# These lines will be executed when this class is imported by main.py
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "localhost"
PORT = 9000 # can be any port number as long as it is the same in Server.java
print("Launched client")
sock.connect((HOST, PORT))
print("Connected to server")

# Handles input from the server with help from input_handler.py
def receive():
	while True:
		message = sock.recv(1024).decode()
		for line in message.splitlines():
			from input_handler import handle_input
			handle_input(line)

# Is called at the start of main.py, making sure the client can continously
# receive messages from the server.
def start_receiving_thread():
	t = threading.Thread(target=receive)
	t.start()

# Can be used to send messages to the server, for example error codes.
def send(message):
	message += "\n"
	sock.sendall(message.encode())