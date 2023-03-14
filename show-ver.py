import sshconnect

print("importing sshconnect module")

ver = sshconnect.send_command("tmsh show sys version")
print(ver)