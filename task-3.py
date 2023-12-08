import time
import socket
import select
# Define the IP addresses and ports of the routers
R1_ip = "192.168.56.101"
R1_port = 22
R2_ip = "192.168.56.130"
R2_port = 22
# Create sockets for connecting to the routers
R1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
R2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the routers
try:
# Connect to router 1
R1_socket.connect((R1_ip, R1_port))
print("Connected to router 1")
# Send OSPF hello message to router 1
hello_message = "Hello, I am router prne."
R1_socket.sendall(hello_message.encode())
# Receive reply from router 1
reply = R1_socket.recv(1024).decode() 
print("Reply from router 1:", reply) 
# Connect to router 2
R2_socket.connect((R2_ip, R2_port))
print("Connected to router 2")
# Send OSPF hello message to router 2
hello_message = "Hello, I am router prne."
R2_socket.sendall(hello_message.encode())
# Receive reply from router 2
reply = R2_socket.recv(1024).decode()
print("Reply from router 2:", reply)
except socket.error:
print("Failed to connect to routers")
finally:
# Close the sockets
R1_socket.close()
R2_socket.close() 
print("Program terminated")
