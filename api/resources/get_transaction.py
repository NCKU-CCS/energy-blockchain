from flask_restful import Resource
from flask import request
from config import app
import iota
import json


class get_transaction (Resource):
    def get(self, name):
        if len(name) != 81:
            return {
                'message': 'Type Not Included!'
            }, 400

        api = iota.Iota(app.config['API_URI'])

        Tx = name
        try:
            data = api.get_trytes(hashes=[Tx])
            transaction = iota.Transaction.from_tryte_string(
                data.get('trytes')[0])

            confirmed = bool(
                list(api.get_latest_inclusion([Tx])['states'].values())[0])

            message = json.loads(
                transaction.signature_message_fragment.decode())
        except:
            return {
                'message': 'Get from Tangle ERROR!'
            }, 403

        return {
            'is_confirmed': confirmed,
            'message': message
        }, 200
