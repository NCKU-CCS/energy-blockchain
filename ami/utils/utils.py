import json

import iota
from flask import current_app

API = iota.Iota(current_app.config.get("API_URI"))


def get_data(transaction_hash):
    data = API.get_trytes(hashes=[transaction_hash])
    transaction = iota.Transaction.from_tryte_string(data.get("trytes")[0])
    message = json.loads(transaction.signature_message_fragment.decode())
    return message


def is_confirmed(transaction_hash):
    confirmed = bool(
        list(API.get_latest_inclusion([transaction_hash])["states"].values())[0]
    )
    return confirmed
