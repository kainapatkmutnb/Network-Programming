from netmiko import ConnectHandler

# Configuration for the switch
SW4 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.120',
    'username': 'cisco',
    'password': 'cisco',
}

try:
    # Establish connection
    with ConnectHandler(**SW4) as net_connect:
        # Send command to show IP interfaces
        output = net_connect.send_command('show ip int brief')
        print(output)
        
        # Send configuration commands
        config_commands = ['int loop 0', 'ip address 1.1.1.1 255.255.255.0']
        output = net_connect.send_config_set(config_commands)
        print(output)

        # Create VLANs 2 to 20
        for n in range(2, 21):
            print(f"Creating VLAN {n}")
            config_commands = [f'vlan {n}', f'name Python_VLAN_{n}']
            output = net_connect.send_config_set(config_commands)
            print(output)

except Exception as e:
    print(f"An error occurred: {e}")