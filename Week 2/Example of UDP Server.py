print('Server is running!!!')
import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

sock.bind((UDP_IP, UDP_PORT))  # Bind with a tuple of (UDP_IP, UDP_PORT)

try:
    while True:
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        print("Received Message: {}".format(data.decode()))  # Print the received data

except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected, closing server...")
    sock.close()
    print("Server closed.")
