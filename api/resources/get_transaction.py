from flask_restful import Resource
from utils.utils import get_data, is_confirmed

class Get_transaction (Resource):
    def get(self, tx_hash):
        if len(tx_hash) != 81:
            return {
                'message': 'Type Not Included!'
            }, 400
        
        try:
            confirmed = is_confirmed(tx_hash)
            message = get_data(tx_hash)

        except:
            return {
                'message': 'Get from Tangle ERROR!'
            }, 403

        return {
            'is_confirmed': confirmed,
            'message': message
        }, 200
