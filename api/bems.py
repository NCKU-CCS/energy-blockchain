# Client
import socket
import sys
import requests
import json
from utils.logging import logging
from config import app

with open('dr.json', 'r') as f:
    json_data = json.load(f)

r = requests.post(
    app.config['API_TX'], json=json_data)
Tx = r.json()['Tx']
# Tx = 'CICBZCYDEABQ9YN9ZMGNBKKQBBWNMIERSGVNVEQ9ZIKNUMODORUNNOILVXYAT9CAVODLZARGVUFR99999'
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    logging.error("Socket Create ERROR!")
    sys.exit(1)

try:
    sock.connect(('', 54321))
except:
    logging.error("Socket Connect ERROR!")
    exit(1)

send_data = str(json.dumps({
    "DR_data": json_data,
    "Tx": Tx
})).encode()
# print("Send Data:", send_data)
sock.send(send_data)
logging.info("Receve: %s" % sock.recv(1024).decode())
sock.close()
