import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QInputDialog
from PyQt5.QtCore import pyqtSignal, QObject

class ChatClientGUI(QWidget):
    message_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.client_socket = None
        self.receive_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chat Client')
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

        self.connect_button = QPushButton('Connect to Server')
        self.connect_button.clicked.connect(self.connect_to_server)
        layout.addWidget(self.connect_button)

        self.leave_button = QPushButton('Leave Room')
        self.leave_button.clicked.connect(self.leave_room)
        self.leave_button.setEnabled(False)
        layout.addWidget(self.leave_button)

        self.setLayout(layout)

        self.message_received.connect(self.display_message)

    def connect_to_server(self):
        server_ip = 'localhost'
        server_port = 80

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((server_ip, server_port))
        except Exception as error:
            self.display_message(f"Error connecting to the server: {error}")
            return

        username, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your username:')
        if ok:
            room, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter the room name:')
            if ok:
                self.client_socket.send(username.encode('utf-8'))
                self.client_socket.send(room.encode('utf-8'))
                self.receive_thread = threading.Thread(target=self.receive_messages)
                self.receive_thread.start()
                self.connect_button.setEnabled(False)
                self.leave_button.setEnabled(True)
                self.display_message(f"Connected to room: {room}")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    self.message_received.emit("Connection to server lost.")
                    break
                self.message_received.emit(message)
            except Exception as error:
                self.message_received.emit(f"Error: {error}")
                break

    def send_message(self):
        message = self.message_input.text()
        if message.lower() == "exit":
            self.client_socket.send(message.encode('utf-8'))
            self.display_message("You have exited the chat.")
            self.client_socket.close()
            self.connect_button.setEnabled(True)
            self.leave_button.setEnabled(False)
        else:
            self.client_socket.send(message.encode('utf-8'))
            self.message_input.clear()

    def leave_room(self):
        if self.client_socket:
            self.client_socket.send("leave".encode('utf-8'))
            self.display_message("You left the room.")
            self.client_socket.close()
            self.connect_button.setEnabled(True)
            self.leave_button.setEnabled(False)

    def display_message(self, message):
        self.chat_display.append(message)

    def closeEvent(self, event):
        if self.client_socket:
            self.client_socket.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatClientGUI()
    ex.show()
    sys.exit(app.exec_())
