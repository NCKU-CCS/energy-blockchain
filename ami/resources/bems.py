from flask_restful import Resource
from flask import request
from models.schema.bems import bems
from helpers import check_ip
import threading
from config import app
from config import ami_cipher, ami_signer
import json
import base64
from tangle import send_to_iota
from Cryptodome.Hash import SHA256

import requests as req
import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)

# Speed test
from datetime import datetime
import csv

class Bems (Resource):
    @check_ip()
    def post(self):
        try:
            data = request.get_json(force='true')
        except:
            return 'error', 400
        # Speed test
        self.speed = ['','','','']

        self.errors = []
        threads = []
        for idx, field in enumerate(data):
            self.errors.append('')
            threads.append(threading.Thread(target=self.process_data, args=(idx, data[field], field)))
            threads[idx].start()
        for i in range(len(threads)):
            threads[i].join()

        # Speed test
        CSV_FILE = open('speed_test.csv','a')
        CSV_WRITER = csv.writer(CSV_FILE)
        CSV_WRITER.writerows([[datetime.now().strftime("%Y-%M-%dT%H:%m:%S"), *self.speed]])
        CSV_FILE.close()
        print("Cost time for each field:", self.speed)

        print('Error message:', self.errors)

        for error in self.errors:
            if len(error) > 0:
                # print(errors)
                return {
                    'message': 'Data Error.'
                }, 400

        return {
            'message': 'ACCEPT',
        }, 200

    def process_data(self, id, data, field):
        upload = []

        for name in data:
            # check table
            if name not in app.config[('BEMS_ACCEPT')]:
                self.errors[id] = 'Type Not Included!'
                continue

            # choose Schema
            target_schema = getattr(bems, name)
            type_schema = target_schema(many=False)

            # check data type
            result = type_schema.load(data[name])
            if len(result.errors) > 0:
                # Data Type Error
                self.errors[id] = result.errors.copy()
                # print(errors)
            else:
                # encrypt
                
                upload_data = json.dumps(
                    {
                        "data": self.encrypt(data[name]),
                        "signature": self.sign(data[name]),
                        "date": data[name]['updated_at']
                    }
                )

                upload.append((name, upload_data.encode()))
        # send data to iota
        # print(upload)
        
        # Original
        # send_to_iota(id, upload, self.get_address(field))

        # Speedt test
        t = send_to_iota(id, upload, self.get_address(field))
        self.speed[id] = t

    def encrypt(self, data):
        text = json.dumps(data)
        cipher_text = base64.b64encode(ami_cipher.encrypt(text.encode()))
        return cipher_text.decode()

    def sign(self, data):
        data_hash = SHA256.new((json.dumps(data)).encode())

        signature = base64.b64encode(ami_signer.sign(data_hash))
        # print(signature)
        return signature.decode()

    def get_address(self, field):
        headers = {'Authorization': 'Bearer %s' % app.config['TOKEN'][field]}
        r = req.post(app.config['API_TX'], headers=headers, verify=False)
        return r.json()['address']