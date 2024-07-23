# Echo Client program
import socket
import sys

HOST = 'localhost'
PORT = 50007
s = None

# ใช้ getaddrinfo เพื่อหาข้อมูลการเชื่อมต่อ
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        continue
    break

# ตรวจสอบการเชื่อมต่อ
if s is None:
    print('Could not open socket')
    sys.exit(1)

# ส่งข้อมูลและรับข้อมูล
with s:
    s.sendall(b'Hello, World')
    data = s.recv(1024)

print('Received', repr(data))
