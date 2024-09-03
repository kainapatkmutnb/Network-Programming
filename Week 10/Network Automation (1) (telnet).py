import telnetlib
import time

# Configuration variables
username = 'cisco'
password = 'cisco'
IP = '192.168.1.116'

try:
    with telnetlib.Telnet(IP) as tn:  # Removed the timeout parameter
        # Read until username prompt and send username
        tn.read_until(b'Username: ')
        tn.write(username.encode('ascii') + b'\n')

        # Read until password prompt and send password
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b'\n')

        # Enter configuration mode and configure interface
        tn.write(b"conf t\n")
        time.sleep(1)
        tn.write(b"int lo 10\n")
        time.sleep(1)
        tn.write(b"ip add 10.10.10.10 255.255.255.255\n")
        time.sleep(1)
        tn.write(b"end\n")
        tn.write(b"exit\n")
        
        # Display the output
        output = tn.read_very_eager().decode('ascii')
        print(output)

except Exception as e:
    print(f"An error occurred: {e}")