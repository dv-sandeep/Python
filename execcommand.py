#import paramiko
import getpass as gp
import time
import sshconnect

# ip = "192.168.8.60"
# user = input("Enter Username: ")
# passwrd = gp.getpass("Enter your password for " + user + " : ")
# cmd = "tmsh show sys version \n"

def exec_cmd(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exec_result = stdout.read().decode()
    print("command executed successfully")
    print(exec_result)
    return exec_result

# conn = sshconnect.connect(ip, user, passwrd)
# exec_cmd(conn, cmd)




