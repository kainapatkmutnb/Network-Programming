print('Server is running!!!')

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    clientsock, address = s.accept()
    print(f"Connection form {address} has been established!")
    clientsock.send(bytes("Welcome To The Server!", "utf-8"))
    clientsock.close()