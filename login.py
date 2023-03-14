import paramiko
import getpass


# host_name = input("Enter FQDN or IP: ") 
user_name = input("Enter your username: ")
pass_word = getpass.getpass("Enter your password: ", stream=False)

def ssh_login(cmd, host_name, user_name=user_name, pass_word=pass_word):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name, username=user_name, password=pass_word)
    
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode()
    return result
    
# output = ssh_login("tmsh show sys version")
# print(output)


