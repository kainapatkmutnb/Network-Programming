import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 5005
MESSAGE = b'Hello World!'

print("UDP Target IP:", UDP_IP)
print("UDP Target Port:", UDP_PORT)
print("Message:", MESSAGE.decode())  # Decode the bytes to string for printing

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

sock.close()  # Close the socket after sending the message