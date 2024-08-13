import asyncio
import datetime
from colorama import init as colorama_init
from colorama import Fore, Style

class ChatServer:
    def __init__(self):
        self.rooms = {}

    async def handle_client(self, reader, writer):
        address = writer.get_extra_info('peername')
        try:
            username = (await reader.read(100)).decode().strip()
            room = (await reader.read(100)).decode().strip()
        except asyncio.IncompleteReadError:
            writer.close()
            await writer.wait_closed()
            return

        username = f"{room} - {username}"

        if room not in self.rooms:
            self.rooms[room] = []

        self.rooms[room].append((writer, room))
        await self.send_to_room(f"{username} has joined", room)

        while True:
            try:
                message = (await reader.read(1024)).decode().strip()
                if not message:
                    break

                if message.lower() == "leave":
                    await self.send_to_room(f"{username} has left the room", room)
                    self.rooms[room].remove((writer, room))
                    writer.close()
                    await writer.wait_closed()
                    return

                if message.lower() == "exit":
                    await self.send_to_room(f"{username} has left the chat", room)
                    self.rooms[room].remove((writer, room))
                    writer.close()
                    await writer.wait_closed()
                    return

                await self.send_to_room(f"{username} : {message}", room)

            except asyncio.CancelledError:
                break
            except ConnectionResetError:
                print(Fore.RED + f"Connection lost with {address}" + Style.RESET_ALL)
                break
            except Exception as e:
                print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
                break

        writer.close()
        await writer.wait_closed()

    async def send_to_room(self, message, room):
        for writer, r in self.rooms[room]:
            if r == room:
                try:
                    writer.write(message.encode('utf-8') + b'\n')
                    await writer.drain()
                except ConnectionResetError:
                    print(Fore.RED + "Connection reset while sending message." + Style.RESET_ALL)
                    writer.close()
                    self.rooms[room].remove((writer, r))
                except Exception as e:
                    print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
                    writer.close()
                    self.rooms[room].remove((writer, r))

    async def main(self):
        server = await asyncio.start_server(self.handle_client, 'localhost', 80)
        addr = server.sockets[0].getsockname()
        print(f"[STATUS] Server started ")

        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    colorama_init(autoreset=True)
    chat_server = ChatServer()
    try:
        asyncio.run(chat_server.main())
    except KeyboardInterrupt:
        print(Fore.RED + "Server interrupted and shutting down." + Style.RESET_ALL)
