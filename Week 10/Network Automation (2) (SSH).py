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

all_devices = [SW4, SW5]

try:
    for device in all_devices:
        with ConnectHandler(**device) as net_connect:
            for n in range(2, 10):
                print(f"Creating VLAN {n}")
                config_commands = [f'vlan {n}', f'name Python_VLAN_{n}']
                output = net_connect.send_config_set(config_commands)
                print(output)

except Exception as e:
    print(f"An error occurred: {e}")