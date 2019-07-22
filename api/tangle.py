from datetime import datetime
import iota
import numpy as np
import logging

from config import app
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s : %(message)s', datefmt='%Y%m%dT%H%M%S')


def send_to_iota(send_data):
    # preparing transactions
    pt = []

    starttime = datetime.now()
    logging.info("START")
    pt.append(iota.ProposedTransaction(address=iota.Address(app.config['TARGETADDRESS']),  # 81 trytes long address
                                       message=iota.TryteString.from_unicode(
        send_data),
        # Up to 27 trytes
        tag=iota.Tag(b'RBTC9D9DCDEAKDCDFD9DSC'),
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
