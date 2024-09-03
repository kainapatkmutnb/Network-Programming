import telnetlib
import time

# Configuration variables
username = 'cisco'
password = 'cisco'
IP = '192.168.1.116'

try:
    with telnetlib.Telnet(IP) as tn:
        # Log in
        tn.read_until(b'Username: ')
        tn.write(username.encode('ascii') + b'\n')

        if password:
            tn.read_until(b'Password: ')
            tn.write(password.encode('ascii') + b'\n')

        # Enter configuration mode
        tn.write(b'conf t\n')
        time.sleep(1)

        # Create VLANs 2 to 9
        for n in range(2, 10):
            tn.write(f'vlan {n}\n'.encode('ascii'))
            tn.write(f'name Python_VLAN_{n}\n'.encode('ascii'))
            time.sleep(1)  # Ensure sufficient time for command execution

        # Exit configuration mode and close connection
        tn.write(b'end\n')
        tn.write(b'exit\n')

        # Display the output
        output = tn.read_very_eager().decode('ascii')
        print(output)

except Exception as e:
    print(f"An error occurred: {e}")