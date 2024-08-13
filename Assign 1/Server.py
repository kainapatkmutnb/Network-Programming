import socket
import threading
import datetime
from colorama import init as colorama_init
from colorama import Fore, Style
import signal
import sys

class ChatServer:
    def __init__(self):
        self.rooms = {}
        self.server = None

    def remove_client(self, client_socket, room):
        for client, r in self.rooms[room]:
            if client == client_socket:
                self.rooms[room].remove((client, r))
                break

    def send_to_room(self, message, room):
        for client, r in self.rooms[room]:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                self.remove_client(client, r)

    def send_to_client(self, message, client_socket):
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            client_socket.close()

    def handle_client(self, client_socket, client_address, username, room):
        ip_client = client_address[0]
        get_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(Fore.GREEN + f"[{get_time}] [STATUS] {ip_client}:{client_address[1]} connected as {username} in {room}" + Style.RESET_ALL)
        
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    disconnect_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(Fore.RED + f"[{disconnect_time}] [STATUS] {client_address} disconnected from room {room}" + Style.RESET_ALL)
                    break

                if message.lower() == "leave":
                    leave_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(Fore.YELLOW + f"[{leave_time}] [STATUS] {username} IP {client_address} has left the room {room}" + Style.RESET_ALL)
                    self.send_to_room(Fore.YELLOW + f"{username} has left the room at {leave_time}" + Style.RESET_ALL, room)
                    self.remove_client(client_socket, room)
                    break

                elif message.lower() == "exit":
                    exit_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(Fore.RED + f"[{exit_time}] [STATUS] {username} IP {client_address} has exited the program" + Style.RESET_ALL)
                    self.send_to_room(Fore.RED + f"{username} has exited the program at {exit_time}" + Style.RESET_ALL, room)
                    self.remove_client(client_socket, room)
                    client_socket.close()
                    return

                for client, r in self.rooms[room]:
                    if client != client_socket:
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        try:
                            client.send(f"[{timestamp}] {username} : {message}".encode('utf-8'))
                        except:
                            client.close()
                            self.remove_client(client, r)
            except:
                break

        client_socket.close()

    def shutdown_server(self, signal_received, frame):
        print(Fore.RED + "\n[STATUS] Shutting down server..." + Style.RESET_ALL)
        if self.server:
            self.server.close()
        for room in self.rooms.values():
            for client_socket, _ in room:
                try:
                    client_socket.close()
                except:
                    pass
        sys.exit(0)

    def main(self):
        signal.signal(signal.SIGINT, self.shutdown_server)  # Handle Ctrl+C
        HOST = 'localhost'
        PORT = 80

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(5)
        print(f"[STATUS] Waiting for connections...")

        while True:
            try:
                client_socket, client_address = self.server.accept()
                
                # Receive username
                username = client_socket.recv(1024).decode('utf-8')

                # Send the list of available rooms to the client
                available_rooms = ", ".join(self.rooms.keys()) if self.rooms else "No rooms available."
                client_socket.send(available_rooms.encode('utf-8'))

                # Receive room name
                room = client_socket.recv(1024).decode('utf-8')

                username = f"{room} - {username}"

                if room not in self.rooms:
                    self.rooms[room] = []

                self.rooms[room].append((client_socket, room))

                join_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.send_to_room(Fore.GREEN + f"[{join_time}] {username} has joined" + Style.RESET_ALL, room)

                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address, username, room))
                client_thread.start()
            except Exception as e:
                print(Fore.RED + f"[ERROR] Server encountered an issue: {e}" + Style.RESET_ALL)
                self.shutdown_server(None, None)

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.main()
