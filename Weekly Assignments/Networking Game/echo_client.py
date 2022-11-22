##
## Author: Kristina Striegnitz
## Author: John Rieffel 
##
## Version: Fall 2022
##
## This is a client for a simple echo application. The client sends a
## message to the server. The servers echoes it back. When the client
## receives the response, it prints it out and shuts down.


import socket

# Create a UDP socket
UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#"cslab-25.union.edu"
base_address = "localhost"
server_address = (base_address, 7000)

# maximum size of messages that can be received
buffer_size = 1024

# Send data
print("sending message")
#message = input(">")
message = "Hello! This is Caleb."
UDP_sock.sendto(message.encode('utf-8'), server_address)

# Receive response
print("waiting to receive response")
response_string, server = UDP_sock.recvfrom(buffer_size)
response_string = response_string.decode('utf-8')
print("response is:", response_string)

# closing socket
UDP_sock.close()