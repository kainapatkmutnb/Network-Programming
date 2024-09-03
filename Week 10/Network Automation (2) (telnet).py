import telnetlib
import time

# Configuration variables
username = 'cisco'
password = 'cisco'
IP = '192.168.1.116'

try:
    # Establish Telnet connection with automatic closure
    with telnetlib.Telnet(IP) as tn:
        # Send username
        tn.read_until(b'Username: ')
        tn.write(username.encode('ascii') + b'\n')

        # Send password if required
        if password:
            tn.read_until(b'Password: ')
            tn.write(password.encode('ascii') + b'\n')

        # Execute command to show IP interface brief
        tn.write(b'sh ip int brief\n')
        time.sleep(1)  # Ensure sufficient time for the command to execute

        # Exit Telnet session
        tn.write(b'exit\n')

        # Print output received from device
        output = tn.read_very_eager().decode('ascii')
        print(output)

except Exception as e:
    print(f"An error occurred: {e}")