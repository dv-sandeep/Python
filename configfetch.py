import viplist
import csv

temp_vip_list = ['ltm', 'virtual', 'test-vip-4433', '{', 'creation-time', '2023-03-02:00:20:08', 'destination', '10.10.20.55:vop', 'ip-protocol', 'tcp', 'last-modified-time', '2023-03-02:00:20:08', 'mask', '255.255.255.255', 'persist', '{', 'test-vip-cookie', '{', 'default', 'yes', '}', '}', 'pool', 'test-pool-4433', 'profiles', '{', 'http', '{', '}', 'serverssl', '{', 'context', 'serverside', '}', 'tcp', '{', '}', 'test-clientssl', '{', 'context', 'clientside', '}', '}', 'source', '0.0.0.0/0', 'source-address-translation', '{', 'type', 'automap', '}', 'translate-address', 'enabled', 'translate-port', 'enabled', 'vs-index', '16', '}']

def persistence_in_vs(temp_vip_list):
    if temp_vip_list.count("persist") > 0:
        persistence_name = temp_vip_list[temp_vip_list.index("persist") + 2]
        print(persistence_name)

    else:
        persistence_name = "None - Check Irule"
        print(persistence_name)

    return persistence_name 

persistence_in_vs(temp_vip_list)

def pool_in_vs(temp_vip_list):
    if temp_vip_list.count("pool") > 0:
        pool_name = temp_vip_list[temp_vip_list.index("pool") + 1]
        print(pool_name)

    else:
        pool_name = "None - Check Irule"
        print(pool_name)

    return pool_name

poolname = pool_in_vs(temp_vip_list)

def clientssl_in_vs(temp_vip_list):
    if temp_vip_list.count("clientside") > 0:
        clientssl_name = temp_vip_list[temp_vip_list.index("clientside") - 3]
        print(clientssl_name)

    else:
        clientssl_name = "None - Check Irule"
        print(clientssl_name)

    return clientssl_name 

clientssl_in_vs(temp_vip_list)

def serverssl_in_vs(temp_vip_list):
    if temp_vip_list.count("serverside") > 0:
        serverssl_name = temp_vip_list[temp_vip_list.index("serverside") - 3]
        print(serverssl_name)

    else:
        serverssl_name = "None - Check Irule"
        print(serverssl_name)

    return serverssl_name 

serverssl_in_vs(temp_vip_list)

with open("Deletion-DED.csv", "r") as f:
    csv_reader = csv.reader(f)
    next(csv_reader)
    for row in csv_reader:
        ip = row[1]
        vip = row[2]
        vip_name, vip_details_list = viplist.vsconfig(ip, vip)
        pool_name, clientssl_name, serverssl_name, persistence_name = pool_in_vs(vip_details_list), clientssl_in_vs(vip_details_list), serverssl_in_vs(vip_details_list), persistence_in_vs(vip_details_list)
        viplist.vs_list.append(vip_details_list)
        print(vip_name)
        print(vip_details_list)

print("**********")
print("**********")
print(pool_name, clientssl_name, serverssl_name, persistence_name)
print("**********")
print("**********")