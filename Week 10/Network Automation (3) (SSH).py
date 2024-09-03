from netmiko import ConnectHandler

# Configuration for the switches
SW4 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.120',
    'username': 'cisco',
    'password': 'cisco',
}

SW5 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.121',
    'username': 'cisco',
    'password': 'cisco',
}

# Read configuration commands from file
file_path = '/Users/watcharachai/Downloads/1_64/Network Programming/W10/swconfig'

try:
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
    
    print(lines)
    
    all_devices = [SW4, SW5]
    
    for device in all_devices:
        try:
            with ConnectHandler(**device) as net_connect:
                output = net_connect.send_config_set(lines)
                print(f"Output for device {device['ip']}:\n{output}")
        
        except Exception as e:
            print(f"Failed to connect or configure device {device['ip']}: {e}")

except FileNotFoundError:
    print(f"The file at {file_path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")