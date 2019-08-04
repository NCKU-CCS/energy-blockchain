import sys
import socket
# import iota
import datetime
import requests
import json
import hashlib
import base64
from utils.logging import logging
from resources.verify import verify_data

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
            accept = verify_data(str(msg["Tx"]), msg['DR_data'])
        except:
            accept = False
            logging.error("verify_data ERROR!")
        if accept:
            logging.info("DR Accept.")
            csock.send(("Server Receive at %s" %
                        datetime.datetime.now()).encode())
        else:
            logging.info("DR Reject.")
            csock.send("Server Reject.".encode())
    csock.close()
