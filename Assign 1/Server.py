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
        if room in self.rooms:
            for client, r in self.rooms[room]:
                if client == client_socket:
                    self.rooms[room].remove((client, r))
                    break

    def send_to_room(self, message, room):
        if room in self.rooms:
            for client, r in self.rooms[room]:
                try:
                    client.send(message.encode('utf-8'))
                except (socket.error, AttributeError) as e:
                    print(Fore.RED + f"[ERROR] Sending to room failed: {e}" + Style.RESET_ALL)
                    client.close()
                    self.remove_client(client, r)

    def send_to_client(self, message, client_socket):
        try:
            client_socket.send(message.encode('utf-8'))
        except (socket.error, AttributeError) as e:
            print(Fore.RED + f"[ERROR] Sending to client failed: {e}" + Style.RESET_ALL)
            client_socket.close()

    def handle_client(self, client_socket, client_address, username, room):
        ip_client = client_address[0]
        print(Fore.GREEN + f"[{self.timestamp()}] [STATUS] {ip_client}:{client_address[1]} connected as {username} in {room}" + Style.RESET_ALL)
        
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    print(Fore.RED + f"[{self.timestamp()}] [STATUS] {client_address} disconnected from room {room}" + Style.RESET_ALL)
                    break

                if message.lower() == "leave":
                    self.handle_leave(client_socket, client_address, username, room)
                    break

                elif message.lower() == "exit":
                    self.handle_exit(client_socket, client_address, username, room)
                    return

                else:
                    self.broadcast_message(client_socket, room, username, message)
            except (socket.error, AttributeError) as e:
                print(Fore.RED + f"[ERROR] {e}" + Style.RESET_ALL)
                break

        client_socket.close()

    def handle_leave(self, client_socket, client_address, username, room):
        leave_time = self.timestamp()
        print(Fore.YELLOW + f"[{leave_time}] [STATUS] {username} IP {client_address} left the room {room}" + Style.RESET_ALL)
        self.send_to_room(Fore.YELLOW + f"[{leave_time}] {username} has left the room" + Style.RESET_ALL, room)
        self.remove_client(client_socket, room)

        # Send available rooms to the client
        available_rooms = ", ".join(self.rooms.keys()) if self.rooms else "No rooms available."
        self.send_to_client(available_rooms, client_socket)

        # Receive new room selection
        new_room = client_socket.recv(1024).decode('utf-8')

        if new_room not in self.rooms:
            self.rooms[new_room] = []

        self.rooms[new_room].append((client_socket, new_room))
        self.send_to_room(Fore.GREEN + f"[{leave_time}] {username} has joined {new_room}" + Style.RESET_ALL, new_room)

        # Continue handling the client in the new room
        self.handle_client(client_socket, client_address, username, new_room)

    def handle_exit(self, client_socket, client_address, username, room):
        exit_time = self.timestamp()
        print(Fore.RED + f"[{exit_time}] [STATUS] {username} IP {client_address} exited the program" + Style.RESET_ALL)
        self.send_to_room(Fore.RED + f"[{exit_time}] {username} exited the program" + Style.RESET_ALL, room)
        self.remove_client(client_socket, room)
        client_socket.close()

    def broadcast_message(self, client_socket, room, username, message):
        timestamp = self.timestamp()
        formatted_message = f"[{timestamp}] {username}: {message}"
        if room in self.rooms:
            for client, r in self.rooms[room]:
                if client != client_socket:
                    try:
                        client.send(formatted_message.encode('utf-8'))
                    except (socket.error, AttributeError) as e:
                        print(Fore.RED + f"[ERROR] Broadcasting message failed: {e}" + Style.RESET_ALL)
                        client.close()
                        self.remove_client(client, r)

    def timestamp(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
                self.send_to_client(available_rooms, client_socket)

                # Receive room name
                room = client_socket.recv(1024).decode('utf-8')

                if room not in self.rooms:
                    self.rooms[room] = []

                self.rooms[room].append((client_socket, room))

                join_time = self.timestamp()
                self.send_to_room(Fore.GREEN + f"[{join_time}] {username} has joined {room}" + Style.RESET_ALL, room)

                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address, username, room))
                client_thread.start()
            except (socket.error, AttributeError) as e:
                print(Fore.RED + f"[ERROR] Server encountered an issue: {e}" + Style.RESET_ALL)
                self.shutdown_server(None, None)

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.main()
