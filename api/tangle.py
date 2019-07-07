from datetime import datetime
import iota
import numpy as np

from config import app


def send_to_iota(send_data):
    # preparing transactions
    pt = []

    starttime = datetime.now()
    print("\n[START]", starttime)
    pt.append(iota.ProposedTransaction(address=iota.Address(app.config['TARGETADDRESS']),  # 81 trytes long address
                                       message=iota.TryteString.from_unicode(
        send_data),
        # Up to 27 trytes
        tag=iota.Tag(b'RBTC9D9DCDEAKDCDFD9DSC'),
        value=0))

    api = iota.Iota(app.config['API_URI'])

    print("[INFO] Preparing/Broadcasting... Wait please...")
    # the whole process initiated in a single call
    FinalBundle = api.send_transfer(depth=3,
                                    transfers=pt,
                                    min_weight_magnitude=14)['bundle']  # it returns a dictionary with a bundle object

    # bundle is broadcasted, let's print it
    print("[DATA]Generated bundle hash: %s" % (FinalBundle.hash))
    print("[DATA]Tail Transaction in the Bundle is a transaction #%s." %
          (FinalBundle.tail_transaction.current_index))

    print("[DATA]List of all transactions in the bundle:\n")
    for txn in FinalBundle:
        print(vars(txn))
        print("")

    endtime = datetime.now()
    print("[FINISH]", endtime)
    print("Cost time: %f s.\n" %
          ((endtime - starttime).seconds+(endtime - starttime).microseconds/10**6))

    return FinalBundle.tail_transaction.hash
