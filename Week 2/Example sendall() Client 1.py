# Echo Client program
import socket

HOST = 'localhost'  # เปลี่ยนเป็น IP ของเซิร์ฟเวอร์ที่คุณรู้จัก
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # ใช้ connect แทน bind
    s.sendall(b'Hello, World')
    data = s.recv(1024)
print('Received', repr(data))
