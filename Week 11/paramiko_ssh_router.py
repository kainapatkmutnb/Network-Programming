import paramiko
import time

# Define the router details
HOST = '192.168.1.122'
USER = 'cisco'
PASSWORD = 'cisco'

def ssh_connect(host, user, password):
    """Establish an SSH connection to the host and return the connection object."""
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username=user, password=password, allow_agent=False, look_for_keys=False)
        print(f"Successfully connected to: {host}")
        return ssh_client
    except Exception as e:
        print(f"Failed to connect to {host}: {str(e)}")
        return None

def send_command(connection, command):
    """Send a command to the remote connection and return the output."""
    try:
        remote_connection = connection.invoke_shell()
        remote_connection.send(command + '\n')
        time.sleep(1)  # Wait for the command to be processed
        output = remote_connection.recv(65535).decode('ascii')
        return output
    except Exception as e:
        print(f"Failed to send command: {str(e)}")
        return None

if __name__ == "__main__":
    # Establish SSH connection
    ssh_client = ssh_connect(HOST, USER, PASSWORD)
    
    if ssh_client:
        # Send commands and get the output
        output = send_command(ssh_client, 'enable')  # Sending 'enable' mode
        if output:
            print(output)
        
        output = send_command(ssh_client, 'show ip interface brief')
        if output:
            print(output)

        # Close the SSH connection
        ssh_client.close()