import sshconnect
import execcommand
import viplist
import time
import logging
import getpass as gp
import csv

file_name = input("DED-Name or path: ")
vsname = []
with open(file_name, 'r') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)
    for line in csv_reader:
        ip = line[1]
        vip = line[2]
        conn = sshconnect.connect(ip, sshconnect.user, sshconnect.passwrd)
        viplist.vip_name
        viplist.vip_raw