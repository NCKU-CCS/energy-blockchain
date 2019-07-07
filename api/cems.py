import sys
import socket
import iota
import datetime
import requests
import json
import hashlib
import base64


def get_data(Tx, data):
    r = requests.get(
        'http://localhost:5000/get_transaction/'+Tx)
    message = r.json()
    # print(message['message'])
    message = json.loads(message['message'])
    json_data = json.dumps(data).encode('utf-8')
    hash_data = hashlib.sha256(
        json_data).hexdigest().encode()
    base64_data = base64.b64encode(hash_data).decode()
    if base64_data == message['value']:
        return True
    else:
        return False


# Socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    sys.stderr.write("[ERROR] %s\n" % "Socket Create ERROR!")
    sys.exit(1)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse tcp
sock.bind(('', 54321))
sock.listen(5)


while True:
    (csock, adr) = sock.accept()
    print("\n[CLIENT] Client Info: ", adr)
    msg = csock.recv(1024).decode()
    msg = json.loads(msg)
    if not msg:
        pass
    else:
        print("[CLIENT] Client send: " + json.dumps(msg))
        print("[TxHASH]", msg["Tx"])
        try:
            accept = get_data(str(msg["Tx"]), msg['DR_data'])
        except:
            accept = False
            print("[ERROR] %s\n" % "get_data ERROR!")
        if accept:
            print("[STATUS] DR Accept.")
            csock.send(("Server Receive at %s\n" %
                        datetime.datetime.now()).encode())
        else:
            print("[STATUS] DR Reject.")
            csock.send("Server Reject.\n".encode())
    csock.close()
