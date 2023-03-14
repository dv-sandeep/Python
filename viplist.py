import login
import csv


vs_list = []

def vipnames():
    file_name = "/home/sandeep/Python-learning/F5-Deletion/Deletion-DED.csv"
    with open(file_name, 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for line in csv_reader:
            ip = line[1]
            vip = line[2]
            # vip = input("Enter the VIP: ")
            find_vs = "tmsh list ltm virtual one-line |grep " + vip + " |gawk '{print $3}'"
            vs = login.ssh_login(find_vs, ip).strip("\n")
            vs_list.append(vs)
            csvheaders = ["Device IP", "VIP", "VS-Name", "Pool", "Client-SSL", "Server-SSL", "Irule", "Persistence"]
            with open("/home/sandeep/Python-learning/F5-Deletion/consolidated-VS.csv", 'a') as ccfile:
                csv_writer = csv.writer(ccfile)
                csv_writer.writerow([ip, vip, vs])
                


    return vs_list

# vipnames()

# print(vs_list)

# def vsconfig():
#     for v in vs_list:
#         vs_out = "tmsh list ltm virtual " + v + " one-line"
#         vs_config = login.ssh_login(vs_out, ip).strip("\n")
#         print(vs_config)
#         temp_vs = vs_config.split()
#     # if ("clientside" in temp_vs) and ("serverside" in temp_vs):
#     #     c_ssl = temp_vs[temp_vs.index("clientside") - 3]
#     #     s_ssl = temp_vs[temp_vs.index("serverside") - 3]

#     if temp_vs.count("clientside") > 0 and temp_vs.count("serverside") > 0 :
#         c_ssl = temp_vs[temp_vs.index("clientside") - 3]
#         s_ssl = temp_vs[temp_vs.index("serverside") - 3]
#         print(c_ssl)
#         print(s_ssl)

#     elif temp_vs.count("clientside") > 0 and temp_vs.count("serverside") <= 0:
#         c_ssl = temp_vs[temp_vs.index("clientside") - 3]
#         print(c_ssl)
#         print("No Server SSl associated")

#     elif temp_vs.count("clientside") <= 0 and temp_vs.count("serverside") <= 0:
#         print("No Client SSl associated")
#         print("No Server SSl associated")
