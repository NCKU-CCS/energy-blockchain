import iota
from config import app
import json

api = iota.Iota(app.config['API_URI'])

def get_data(transaction_hash):
    data = api.get_trytes(hashes=[transaction_hash])
    transaction = iota.Transaction.from_tryte_string(data.get('trytes')[0])
    message = json.loads(transaction.signature_message_fragment.decode())
    return message

def is_confirmed(transaction_hash):
    confirmed = bool(list(api.get_latest_inclusion([transaction_hash])['states'].values())[0])
    return confirmed