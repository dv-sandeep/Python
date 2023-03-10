import paramiko
import sys
import subprocess
import logging
import getpass as gp
import time

# ip = "192.168.8.60"
user = input("Enter Username: ")
passwrd = gp.getpass("Enter your password for " + user + " : ")

def connect(host_name, user_name=user, pass_word=passwrd):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'Connecting to *****{host_name}*****')
    ssh_client.connect(hostname=host_name, username=user_name, password=pass_word, look_for_keys=False, allow_agent=False)
    return ssh_client

def get_shell(ssh_client):
    shell = ssh_client.invoke_shell()
    return shell

def send_command(shell, command, timeout=2):
    print(f'sending command: {command}')
    shell.send(command + '\n')
    time.sleep(timeout)
    output = shell.recv(n)
    return output.decode()