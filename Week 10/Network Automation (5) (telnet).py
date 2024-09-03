import telnetlib

# Configuration variables
username = 'cisco'
password = 'cisco'

try:
    with open('myswitches', 'r') as f:
        for line in f:
            IP = line.strip()  # Remove any surrounding whitespace/newlines
            print(f"Configuring Switch IP = {IP}")

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

                    # Create VLANs 2 to 9
                    for n in range(2, 10):
                        tn.write(f'vlan {n}\n'.encode('ascii'))
                        tn.write(f'name Python_VLAN_{n}\n'.encode('ascii'))
                    
                    # Exit configuration mode and close connection
                    tn.write(b'end\n')
                    tn.write(b'exit\n')

                    # Display the output
                    output = tn.read_all().decode('ascii')
                    print(output)

            except Exception as e:
                print(f"Failed to configure switch {IP}: {e}")

except FileNotFoundError:
    print("The file 'myswitches' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")