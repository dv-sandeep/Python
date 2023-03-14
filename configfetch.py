import viplist
import login
import csv

viplist.vipnames()

virtual_dict = {}
with open("/home/sandeep/Python-learning/F5-Deletion/consolidated-VS.csv") as vscsv:
    vscsv_reader = csv.reader(vscsv)
    for line in vscsv_reader:
        ip = line[0]
        vserver = line[2]
        vs_config_cmd = "tmsh list ltm virtual " + vserver + " one-line"
        vs_config = login.ssh_login(vs_config_cmd, ip).strip("\n")
        temp_vs = vs_config.split()

        if temp_vs.count("clientside") > 0 and temp_vs.count("serverside") > 0 :
            c_ssl = temp_vs[temp_vs.index("clientside") - 3]
            s_ssl = temp_vs[temp_vs.index("serverside") - 3]
            print(c_ssl)
            print(s_ssl)
            vip_dict = {{ip:vserver}, {"ClientSSL":c_ssl}, {"ServerSSl":s_ssl}}
            virtual_dict.update(vip_dict)

        elif temp_vs.count("clientside") > 0 and temp_vs.count("serverside") <= 0:
            c_ssl = temp_vs[temp_vs.index("clientside") - 3]
            print(c_ssl)
            print("No Server SSl associated")
            vip_dict = [{ip:vserver}, {"ClientSSL":c_ssl}, {"ServerSSl":"No Server SSL"}]
            virtual_dict.update(vip_dict)

        elif temp_vs.count("clientside") <= 0 and temp_vs.count("serverside") <= 0:
            print("No Client SSl associated")
            print("No Server SSl associated")
            vip_dict = [{ip:vserver}, {"ClientSSL":"No Client SSL"}, {"ServerSSl":"No Server SSL"}]
            virtual_dict.update(vip_dict)

print(virtual_dict)



