import json
import base64
import threading

import requests as req
from flask import request, current_app
from flask_restful import Resource
from loguru import logger
from Cryptodome.Hash import SHA256

from config import AMI_CIPHER as ami_cipher
from config import AMI_SIGNER as ami_signer
from utils.tangle import Iota
from utils.helpers import check_ip
from models.schema.bems import bems


class Bems(Resource):
    def __init__(self):
        self.app = current_app
        self.bems_accept = current_app.config["BEMS_ACCEPT"]
        self.token = current_app.config["TOKEN"]
        self.api_get_address = current_app.config["API_TX"]
        self.errors = None

    @check_ip()
    def post(self):
        # if json decode error will return None
        data = request.get_json()
        # data = request.get_json(silent=True)
        if not data:
            return {"message": "JSON data error"}, 400

        threads = []
        self.errors = []
        for idx, field in enumerate(data):
            self.errors.append("")
            threads.append(
                threading.Thread(
                    target=self.process_data, args=(idx, data[field], field)
                )
            )
            threads[idx].start()
        for num, _ in enumerate(threads):
            threads[num].join()

        if any(self.errors):
            return {"message": self.errors}, 403

        return {"message": "ACCEPT"}, 200

    def process_data(self, idx, data, field):
        """check data and consolidated data

        Arguments:
            idx {int} -- idx of thread
            data {dict} -- data of one field
            field {string} -- field name
        """
        # check field name is correct
        if field not in self.token:
            self.errors[idx] = "Field Not Included!"
            return

        upload_datas = []
        # check data_table name is correct
        for data_table in data:
            if data_table not in self.bems_accept:
                self.errors[idx] = "Type Not Included!"
                return

            # choose Schema
            target_schema = getattr(bems, data_table)
            type_schema = target_schema(many=False)

            # check data type
            result = type_schema.load(data[data_table])
            if result.errors:
                # Data Type Error
                self.errors[idx] = result.errors.copy()
                return

            # encrypt
            upload_data = json.dumps(
                {
                    "id": data[data_table]["id"],
                    "data": self.encrypt(data[data_table]),
                    "signature": self.sign(data[data_table]),
                }
            )
            upload_datas.append((data_table, upload_data.encode()))

        iota = Iota()
        bundle_hash, cost_time = iota.send_to_iota(
            upload_datas, self.get_address(field)
        )
        logger.info(
            f"AMI: {field}\nAMI Data: {data}\nBundle Hash: {bundle_hash}\nCost time: {cost_time}\n"
        )

    @staticmethod
    def encrypt(data):
        """encrypt data"""
        text = json.dumps(data)
        cipher_text = base64.b64encode(ami_cipher.encrypt(text.encode()))
        return cipher_text.decode()

    @staticmethod
    def sign(data):
        """calculate data's signature"""
        data_hash = SHA256.new((json.dumps(data)).encode())
        signature = base64.b64encode(ami_signer.sign(data_hash))
        return signature.decode()

    def get_address(self, field):
        """get iota receiving address from platform"""
        headers = {"Authorization": "Bearer %s" % self.token[field]}
        response = req.get(self.api_get_address, headers=headers)
        return response.json()["address"]
