import logging
import socket
import select

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

# Non Blocking
def create_non_blocking(host, port):
    logging.info('Non Blocking - Creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    logging.info(f'Non Blocking - Connecting to {host}:{port}')
    ret = s.connect_ex((host, port))  # Blocking call

    if ret != 0:
        logging.error('Non Blocking - Failed to connect!')
        return
    
    logging.info('Non Blocking - Connected!')
    s.setblocking(False)

    inputs = [s]
    outputs = [s]

    while inputs:
        logging.info('Non Blocking - Waiting')
        readable, writable, exceptional = select.select(inputs, outputs, inputs, 0.5)

        for sock in writable:
            logging.info('Non Blocking - Sending...')
            data = sock.send(b'hello\r\n')
            logging.info(f'Non Blocking - Sent: {data} bytes')
            outputs.remove(sock)

        for sock in readable:
            logging.info('Non Blocking - Reading...')
            data = sock.recv(1024)
            logging.info(f'Non Blocking - Data: {len(data)}')
            logging.info('Non Blocking - Closing...')
            sock.close()
            inputs.remove(sock)

        for sock in exceptional:
            logging.error('Non Blocking - Exceptional condition')
            inputs.remove(sock)
            outputs.remove(sock)

def main():
    create_non_blocking('voidrealms.com', 80)

if __name__ == "__main__":
    main()
