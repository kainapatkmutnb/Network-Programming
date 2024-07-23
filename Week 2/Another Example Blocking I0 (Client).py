import logging
import socket

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

# Blocking
def create_blocking(host, port):
    logging.info('Blocking - Creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    logging.info(f'Blocking - Connecting to {host}:{port}')
    s.connect((host, port))

    logging.info('Blocking - Sending...')
    s.send(b'hello\r\n')

    logging.info('Blocking - Waiting...')
    data = s.recv(1024)
    logging.info(f'Blocking - data= {len(data)}')
    
    logging.info('Blocking - Closing')
    s.close()

def main():
    create_blocking('voidrealms.com', 80)

if __name__ == "__main__":
    main()
