import sshconnect
import execcommand
import csv
import getpass as gp

def vip_name(vip):
    vip_name_cmd = "tmsh list ltm virtual one-line |grep " + vip + " |gawk {'print $3'}"
    # conn = sshconnect.connect(sshconnect.ip, sshconnect.user, sshconnect.passwrd)
    print("connected")
    vs_name = execcommand.exec_cmd(sshconnect.connect, vip_name_cmd)
    return vs_name

# vs_raw = vip_name("10.10.20.55:vop")
# print(vs_raw)

def vip_raw(vs_name):
    vs_cmd = "tmsh list ltm virtual " + vs_name + ""
    # conn = sshconnect.connect(sshconnect.ip, sshconnect.user, sshconnect.passwrd)
    list_vs = execcommand.exec_cmd(sshconnect.connect, vs_cmd)
    return list_vs 

def vip_pool(vs_name):
    vs_pool_cmd = "tmsh list ltm virtual " + vs_name + " |grep pool"
    # conn = sshconnect.connect(sshconnect.ip, sshconnect.user, sshconnect.passwrd)
    list_vs_pool = execcommand.exec_cmd(sshconnect.connect, vs_pool_cmd)
    if len(list_vs_pool) == 0:
        print("The virtual " + vs_name + " doesn't have any pool assigned")
    else:
        print("The virtual " + vs_name + " have a pool assigned " + list_vs_pool + "")
    return list_vs_pool 

# def vip_clientssl(vs_name):
#     vs_clientssl_cmd = "tmsh list ltm virtual " + vs_name + " |grep client-ssl"

