import sys
import socket
# import iota
import datetime
import requests
import json
import hashlib
import base64
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s : %(message)s', datefmt='%Y%m%dT%H%M%S')


def get_data(Tx, data):
    r = requests.get(
        'http://localhost:5000/get_transaction/'+Tx)
    message = r.json()
    json_data = json.dumps(data).encode('utf-8')
    hash_data = hashlib.sha256(
        json_data).hexdigest().encode()
    base64_data = base64.b64encode(hash_data).decode()
    if base64_data == message['message']['value']:
        return True
    else:
        return False


# Socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    logging.error("Socket Create ERROR!")
    sys.exit(1)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse tcp
sock.bind(('', 54321))
sock.listen(5)


while True:
    (csock, adr) = sock.accept()
    logging.info("Client Info: %s" % str(adr))
    msg = csock.recv(1024).decode()
    msg = json.loads(msg)
    if not msg:
        pass
    else:
        logging.info("Client send: " + json.dumps(msg))
        logging.info("TxHASH: %s" % msg["Tx"])
        try:
            accept = get_data(str(msg["Tx"]), msg['DR_data'])
        except:
            accept = False
            logging.error("get_data ERROR!")
        if accept:
            logging.info("DR Accept.")
            csock.send(("Server Receive at %s\n" %
                        datetime.datetime.now()).encode())
        else:
            logging.info("DR Reject.")
            csock.send("Server Reject.\n".encode())
    csock.close()
