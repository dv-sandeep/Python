import sshconnect
import execcommand
import time
import logging
import getpass as gp
import csv

file_name = input("DED-Name or path: ")

with open(file_name, 'r') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)
    for line in csv_reader:
        ip = line[1]
        vip = line[2]
