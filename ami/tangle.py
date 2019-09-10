from datetime import datetime
import iota
import numpy as np
from utils.logging import logging
from config import app

TARGETADDRESS = b'HPKOGKEJYBU9DJACHWVSIBHBSBCNPVCOAFRPSSELCRQFCRSHVMNGWWG9AH9JOFHAOHWTFAYTMMKJJCAS9'

def send_to_iota(send_data):
    # preparing transactions
    pt = []

    starttime = datetime.now()
    logging.info("START")
    for tag, data in send_data:
        pt.append(iota.ProposedTransaction(address=iota.Address(TARGETADDRESS),  # 81 trytes long address
                                        message=iota.TryteString.from_bytes(
            data),
            # Up to 27 trytes
            tag=iota.Tag(get_tag(tag).encode()),
            value=0))

    api = iota.Iota(app.config['API_URI'])

    logging.info("Preparing/Broadcasting... Wait please...")
    # the whole process initiated in a single call
    FinalBundle = api.send_transfer(depth=3,
                                    transfers=pt,
                                    min_weight_magnitude=14)['bundle']  # it returns a dictionary with a bundle object

    # bundle is broadcasted, let's print it
    logging.info("Generated bundle hash: %s" % (FinalBundle.hash))
    logging.info("Tail Transaction in the Bundle is a transaction #%s." %
                 (FinalBundle.tail_transaction.current_index))

    logging.info("List of all transactions in the bundle:\n")
    for txn in FinalBundle:
        logging.info(vars(txn))

    endtime = datetime.now()
    logging.info("FINISH")
    logging.info("Cost time: %f s.\n" %
                 ((endtime - starttime).seconds+(endtime - starttime).microseconds/10**6))

    return FinalBundle.tail_transaction.hash

def get_tag(text):
    tag = text.upper().replace('_', '9')
    tag += '9' + chr(ord('A') + datetime.now().hour)
    print(tag)
    return tag

def get_address():
    # get address from platform
    pass