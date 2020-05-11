from datetime import datetime

import requests
import iota
from loguru import logger

from config import API_URI, API_OPEN


class Iota:
    def __init__(self):
        self.api_uri = API_URI
        self.api_open = API_OPEN
        self.api_entry = self.get_api_entry()

    def get_api_entry(self):
        """return usable api entry"""
        get_api = False
        for api_uri in self.api_uri:
            logger.info(f"[URI] testing {api_uri}")
            # Check if the node is available and up to date
            try:
                api_entry = iota.Iota(api_uri)
                node_info = api_entry.get_node_info()
                if node_info["latestMilestone"] == node_info["latestSolidSubtangleMilestone"]:
                    get_api = True
                    break
            except requests.exceptions.ConnectionError:
                logger.warning(f"URI {api_uri} is down.")
        if get_api is False:
            logger.warning("ALL NODES DOWN\nUsing Open Nodes.")
            api_entry = iota.Iota(self.api_open)
        return api_entry

    @staticmethod
    def get_tag(text):
        """transfer tag to IOTA TAG which accept A-Z and 9

        Arguments:
            text {string} -- type of data

        Returns:
            string -- IOTA TAG
        """
        # add timestamp
        text += f"_{chr(ord('A') + datetime.utcnow().hour)}"
        # tranfer to uppercase and use `9` to replace `_`
        tag = text.upper().replace("_", "9")
        return tag

    def send_to_iota(self, send_data, target_address):
        """transfer data to the Tangle

        Arguments:
            send_data {list} -- five pair of tag and upload data with string type
            target_address {string} -- iota receive address

        Returns:
            iota.transaction.types.BundleHash -- BundleHash of the transaction
            datetime.timedelta -- cost time
        """
        # preparing transactions
        transactions = []
        for tag, data in send_data:
            transactions.append(
                iota.ProposedTransaction(
                    address=iota.Address(target_address),
                    message=iota.TryteString.from_bytes(data),
                    tag=iota.Tag(self.get_tag(tag).encode()),
                    value=0,
                )
            )

        start_time = datetime.now()
        final_bundle = self.api_entry.send_transfer(transfers=transactions)["bundle"]
        end_time = datetime.now()

        return final_bundle.hash, end_time - start_time
