import sshconnect
import execcommand
import csv
import getpass as gp

ip = "192.168.8.60"
user = input("Enter username: ")
passwd = gp.getpass("Enter Password: ", stream=False)
cmd = input("Enter the command: ")

conn = sshconnect.connect(ip, user, passwd)
execcommand.exec_cmd(conn, cmd)
