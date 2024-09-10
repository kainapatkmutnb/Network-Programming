import paramiko
import threading
import os
import subprocess
import time
import sys
import re

############# Application #2 - Part #1 #############

# Function to check the validity of IP addresses
def ip_is_valid(ip_list):
    while True:
        check = True
        for ip in ip_list:
            a = ip.strip().split('.')
            if (len(a) == 4 and
                1 <= int(a[0]) <= 223 and
                int(a[0]) != 127 and
                not (int(a[0]) == 169 and int(a[1]) == 254) and
                all(0 <= int(octet) <= 255 for octet in a)):
                continue
            else:
                print(f"Invalid IP address: {'.'.join(a)}")
                check = False
                break
        if check:
            print("All IP addresses are valid.")
            break
        else:
            print("Please check the IP address list and try again.")
            ip_list = input("Enter IP file name and extension: ").strip()
            with open(ip_list, 'r') as file:
                ip_list = file.readlines()

############# Application #2 - Part #2 #############

# Function to check IP reachability
def check_ip_reachability(ip_list):
    while True:
        check2 = True
        for ip in ip_list:
            ping_reply = subprocess.call(["ping", "-c", "2", "-W", "1", ip.strip()])
            if ping_reply != 0:
                print(f"Ping to {ip.strip()} failed.")
                check2 = False
                break
        if check2:
            print("All devices are reachable.")
            break
        else:
            print("Please re-check the IP address list or devices.")
            ip_list = input("Enter IP file name and extension: ").strip()
            with open(ip_list, 'r') as file:
                ip_list = file.readlines()

############# Application #2 - Part #3 #############

# Function to validate the user file
def user_is_valid():
    while True:
        user_file = input("Enter user/pass file name and extension: ").strip()
        if os.path.isfile(user_file):
            print("Username/password file validated.")
            return user_file
        else:
            print(f"File {user_file} does not exist. Please check and try again.")

# Function to validate the command file
def cmd_is_valid():
    while True:
        cmd_file = input("Enter command file name and extension: ").strip()
        if os.path.isfile(cmd_file):
            print("Command file validated.")
            return cmd_file
        else:
            print(f"File {cmd_file} does not exist. Please check and try again.")

############# Application #2 - Part #4 #############

# Function to open SSH connection and execute commands
def open_ssh_conn(ip, user_file, cmd_file):
    try:
        with open(user_file, 'r') as file:
            username, password = file.readline().strip().split(',')

        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(ip, username=username, password=password, allow_agent=False, look_for_keys=False)
        connection = session.invoke_shell()

        with open(cmd_file, 'r') as file:
            for line in file:
                connection.send(line + '\n')
                time.sleep(2)

        router_output = connection.recv(65535).decode('utf-8')
        if re.search(r"% Invalid input detected at", router_output):
            print(f"Error on device {ip}: {router_output}")
        else:
            print(f"Commands executed successfully on device {ip}.")
            print(router_output)

        session.close()
    except paramiko.AuthenticationException:
        print(f"Authentication failed for device {ip}.")
    except Exception as e:
        print(f"Error with device {ip}: {e}")

############# Application #2 - Part #5 #############

# Function to create and start threads for SSH connections
def create_threads(ip_list, user_file, cmd_file):
    threads = []
    for ip in ip_list:
        th = threading.Thread(target=open_ssh_conn, args=(ip.strip(), user_file, cmd_file))
        th.start()
        threads.append(th)
    for th in threads:
        th.join()

if __name__ == "__main__":
    try:
        ip_file = input("Enter IP file name and extension: ").strip()
        with open(ip_file, 'r') as file:
            ip_list = file.readlines()

        ip_is_valid(ip_list)
        check_ip_reachability(ip_list)
        user_file = user_is_valid()
        cmd_file = cmd_is_valid()
        create_threads(ip_list, user_file, cmd_file)
    except KeyboardInterrupt:
        print("\nProgram aborted by user. Exiting...")
        sys.exit()
    except FileNotFoundError as e:
        print(f"File error: {e}")
        sys.exit()