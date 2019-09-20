import socket
import sys
import requests
import json
import threading
import time


API_TX = 'https://127.0.0.1:4000/bems/upload'

with open('../test/json/upload.json', 'r') as f:
    json_data = json.load(f)

def req():
    r = requests.post(API_TX, json=json_data, verify=False)
    print(r.json())
    print('-'*60)

threads = []
for idx in range(120):
    print(time.asctime(time.localtime(time.time())))
    threads.append(threading.Thread(target=req))
    threads[idx].start()
    time.sleep(60)



