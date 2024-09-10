import threading
from queue import Queue
from netmiko import ConnectHandler

# Define username and password to login to all routers with
USER = 'cisco'
PASSWORD = 'cisco'

# Define router IPs
routers = ['192.168.1.122', '192.168.1.123', '192.168.1.124']

def ssh_session(router, output_q):
    # Create a dictionary to store the output for each router
    output_dict = {}
    hostname = router
    device_params = {
        'device_type': 'cisco_ios',
        'ip': router,
        'username': USER,
        'password': PASSWORD,
        'verbose': False
    }
    # Connect to the router via SSH
    ssh_session = ConnectHandler(**device_params)
    # Execute the command and store the output
    output = ssh_session.send_command("show version")
    output_dict[hostname] = output
    output_q.put(output_dict)

if __name__ == "__main__":
    output_q = Queue()

    # Start thread for each router in routers list
    threads = []
    for router in routers:
        my_thread = threading.Thread(target=ssh_session, args=(router, output_q))
        my_thread.start()
        threads.append(my_thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Retrieve everything from the queue and print the output
    while not output_q.empty():
        my_dict = output_q.get()
        for hostname, output in my_dict.items():
            print(f"Router: {hostname}")
            print(output)