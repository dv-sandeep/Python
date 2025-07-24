#!/usr/bin/python
#!/home/sandeep/Automation/F5-Scripts/env/bin/python

"""
Version: 3
Author: Venkata Sandeep
Description: Run precheck commands on F5/Firewall devices. Output is saved to the user's home directory.
"""

import paramiko
import getpass
import time
import datetime
import os
import concurrent.futures
from functools import partial

# Terminal color codes
RED, GREEN, YELLOW, RESET = "\033[0;31m", "\033[0;32m", "\033[0;33m", "\033[0m"

PROMPTS = ["#", ">", "~", "$"]
RESTRICTED_COMMANDS = ["delete", "restart", "shutdown", "modify", "reboot", "decommission", "remove"]

print(f"""{YELLOW}
You are about to run precheck commands on Single/Multiple Production/Non-Production Devices.
Ensure your CHANGE is fully approved in ServiceNow and in 'Implementation' state.
{RESET}""")

CHANGE_NUMBER = input(f"{YELLOW}Please provide valid CHANGE NUMBER:{GREEN} ")
CURRENT_DATE = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
CHECKS_TYPE = input(f"{YELLOW}PRE-CHECK or POST-CHECK: ")

def output_file(host):
    dir_path = os.path.join(os.path.expanduser(f"~{getpass.getuser()}"), f"{CHANGE_NUMBER}/{CHECKS_TYPE}")
    os.makedirs(dir_path, exist_ok=True)
    path = os.path.join(dir_path, f"{host}_{CURRENT_DATE}.txt")
    return path

def user_options():
    while True:
        print(f"""{YELLOW}
Welcome! This script will run command(s) on F5 or Firewall and capture the output.
{GREEN}
1. Firewall
2. F5-BASH
3. Quit
{RESET}
""")
        user_selection = input(f"{YELLOW}Select an option:{GREEN} ").strip()
        if user_selection in ["1", "2"]:
            print(f"{YELLOW}\nYou selected: {GREEN}{'Firewall' if user_selection == '1' else 'F5-BASH'}{RESET}\n")
            return user_selection
        elif user_selection == "3":
            print(f"{RED}\nYou chose to quit. Exiting...{RESET}")
            exit(0)
        else:
            print(f"{RED}Invalid option. Try again.{RESET}")

def user_command():
    print(f"""{YELLOW}
Enter the commands to execute. Type {GREEN}DONE{YELLOW} when finished.
{RESET}""")
    user_cmds = []
    while True:
        try:
            line = input(f"{GREEN}").strip()
            if line.upper() == "DONE":
                break
            elif any(cmd in line for cmd in RESTRICTED_COMMANDS):
                print(f"{RED}Restricted command detected: {line}{RESET}")
                break
            elif line:
                user_cmds.append(line)
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")
            break
    return user_cmds

def devices_provided_by_user():
    print(f"""{YELLOW}
Enter the list of devices. Type {GREEN}DONE{YELLOW} when finished.
{RESET}""")
    devices = []
    while True:
        try:
            line = input(f"{GREEN}").strip()
            if line.upper() == "DONE":
                break
            elif line:
                devices.extend(line.replace(',', ' ').split())
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")
            break
    return devices

def ssh_to_host(host, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"{YELLOW}Connecting to {GREEN}{host}{YELLOW} as {GREEN}{username}{YELLOW}...{RESET}")
        ssh.connect(host, username=username, password=password)
        return ssh
    except paramiko.AuthenticationException:
        print(f"{RED}Authentication failed for {host}.{RESET}")
    except paramiko.SSHException as e:
        print(f"{RED}SSH error on {host}: {e}{RESET}")
    except Exception as e:
        print(f"{RED}Connection error on {host}: {e}{RESET}")
    return None

def ssh_close(ssh):
    if ssh:
        ssh.close()

def invoke_shell(ssh, user_cmds, pre_cmd=None):
    buffer = ''
    if not ssh:
        return buffer
    channel = ssh.invoke_shell()
    if pre_cmd:
        channel.send(pre_cmd + '\n')
        time.sleep(1)

    for cmd in user_cmds:
        print(f"{YELLOW}Executing: {GREEN}{cmd}{RESET}")
        channel.send(cmd + '\n')
        time.sleep(1)
        while True:
            if channel.recv_ready():
                data = channel.recv(65535).decode('utf-8')
                buffer += data
                if any(buffer.strip().endswith(prompt) for prompt in PROMPTS):
                    break
            else:
                time.sleep(1)
    return buffer

def write_to_file(file, output):
    try:
        with open(file, 'a') as wf:
            wf.write(output + '\n')
    except Exception as e:
        print(f"{RED}Error writing to file {file}: {e}{RESET}")

def precheck_execution(host, user_selection, user_name, user_password, user_cmds):
    file_path = output_file(host)
    header = f"\n{'='*len(host)} {host} {'='*len(host)}\n"
    write_to_file(file_path, header)

    ssh = ssh_to_host(host, user_name, user_password)
    if not ssh:
        return

    try:
        if user_selection == "1":  # Firewall
            output = invoke_shell(ssh, user_cmds, pre_cmd='terminal length 0')
        elif user_selection == "2":  # F5-BASH
            output = invoke_shell(ssh, user_cmds, pre_cmd='run /util bash')
        else:
            output = ""
        print(f"{GREEN}{output}{RESET}")
        write_to_file(file_path, output)
    finally:
        ssh_close(ssh)
        print(f"{RED}\nOutput saved to: {GREEN}{file_path}{RESET}\n")

def summary_of_selection(user_selection, devices, user_cmds, user_name):
    type_map = {"1": "FIREWALL", "2": "F5-BASH"}
    print(f"""{YELLOW}
SUMMARY:
    Change Number     : {GREEN}{CHANGE_NUMBER}
    Device Type       : {GREEN}{type_map.get(user_selection, 'Unknown')}
    Devices           : {GREEN}{devices}
    Commands          : {GREEN}{user_cmds}
    Username          : {GREEN}{user_name}
{RESET}
""")

def main():
    user_selection = user_options()
    devices = devices_provided_by_user()

    if not devices:
        print(f"{RED}No devices provided. Exiting...{RESET}")
        return

    user_cmds = user_command()
    if not user_cmds:
        print(f"{RED}No commands provided. Exiting...{RESET}")
        return

    user_name = input(f"\n{YELLOW}Enter your username:{GREEN} ").strip()
    user_password = getpass.getpass(f"{YELLOW}Enter password for {GREEN}{user_name}{YELLOW}: {RESET}")

    summary_of_selection(user_selection, devices, user_cmds, user_name)

    start_time = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(
            partial(precheck_execution,
                    user_selection=user_selection,
                    user_name=user_name,
                    user_password=user_password,
                    user_cmds=user_cmds),
            devices
        )
    end_time = time.perf_counter()
    print(f"\n{RED}Script completed in {GREEN}{end_time - start_time:.2f}{RED} seconds.{RESET}")

if __name__ == "__main__":
    main()
