import asyncio
from colorama import init as colorama_init
from colorama import Fore, Style

async def receive_messages(reader):
    while True:
        try:
            message = await reader.read(1024)
            if not message:
                print(Fore.RED + "Connection to server lost." + Style.RESET_ALL)
                break
            print(message.decode().strip())
        except Exception as error:
            print(Fore.RED + f"Error: {error}" + Style.RESET_ALL)
            break

async def main():
    colorama_init(autoreset=True)
    server_ip = 'localhost'
    server_port = 80

    reader, writer = await asyncio.open_connection(server_ip, server_port)

    NAME = input("Enter your username: ")

    while True:
        print("")
        print("You can create a room or type 'exit' to quit")
        print("")

        room = input("Enter the room name: ")

        if room.lower() == "exit":
            writer.write(room.encode('utf-8') + b'\n')
            await writer.drain()
            print(Fore.RED + "You have exited the server." + Style.RESET_ALL)
            writer.close()
            await writer.wait_closed()
            break

        print("")
        print("You can create a room or type 'leave' to leave room")
        print("")

        writer.write(NAME.encode('utf-8') + b'\n')
        writer.write(room.encode('utf-8') + b'\n')
        await writer.drain()

        asyncio.create_task(receive_messages(reader))

        while True:
            message = input("")

            if message.lower() == "exit":
                writer.write(message.encode('utf-8') + b'\n')
                await writer.drain()
                print(Fore.RED + "You have exited the chat." + Style.RESET_ALL)
                writer.close()
                await writer.wait_closed()
                return
            elif message.lower() == "leave":
                writer.write(message.encode('utf-8') + b'\n')
                await writer.drain()
                print(Fore.YELLOW + f"{NAME} left the chat" + Style.RESET_ALL)
                writer.close()
                await writer.wait_closed()
                return
            else:
                print(Fore.GREEN + f"{room} - {NAME} sent message: {message}" + Style.RESET_ALL)
                writer.write(message.encode('utf-8') + b'\n')
                await writer.drain()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "Client interrupted and shutting down." + Style.RESET_ALL)
