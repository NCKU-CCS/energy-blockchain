# Client
import socket
import sys
import requests
import json
from utils.logging import logging

json_data = {
    "id": 29,
    "field": "NCKU",
    "eventID": "c14164d1a259670a0338",
    "eventdate": "2019-05-06T00:00:00",
    "bidding_price": 1.254,
    "bidding_capacity": 8.0,
    "get_bidding": 1,
    "amount": 8.0,
    "start_at": "2019-05-06 17:00:00",
    "end_at": "2019-05-06 17:15:00",
    "baseline": -1.0,
    "max_consumption": -1.0,
    "actual_load_shedding": -1.0,
    "expected_reward": -1.0,
    "actual_reward": -1.0,
    "feedback_ratio": -1.0,
    "result": -1.0,
    "inserted_at": "2019-05-03T00:00:24"
}

r = requests.post(
    'http://localhost:5000/hems/aggregator_dr_event', json=json_data)
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
