import sshconnect
import execcommand
import csv
import getpass as gp

def vip_info(vip):
    vip_name = "tmsh list ltm virtual one-line |grep " + vip + " | gawk {'print $3'}"
    conn = sshconnect.connect(sshconnect.ip, sshconnect.user, sshconnect.passwrd)
    vs_name = execcommand.exec_cmd(conn, vip_name)
    return vs_name
