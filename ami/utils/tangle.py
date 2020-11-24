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
        available_nodes = list()
        for node in self.api_uri:
            logger.info(f"[CHECK NODES] Testing {node}")
            try:
                api = iota.Iota(iota.HttpAdapter(node, timeout=5))
                # Check node alive
                node_info = api.get_node_info()
                # Show Node Info
                logger.debug(node_info)
                # Check node milestone is latest
                assert node_info["latestMilestone"] == node_info["latestSolidSubtangleMilestone"]
                logger.success(f"[CHECK NODES] Node is alive. URI: {node}")
                available_nodes.append(node)
            except AssertionError:
                logger.warning(f"[CHECK NODES] Node is not up to date. URI: {node}")
            except requests.exceptions.ConnectionError:
                logger.error(f"[CHECK NODES] Node is down. URI: {node}")
            except requests.exceptions.ReadTimeout:
                logger.error(f"[CHECK NODES] Node timeout. URI: {node}")
        if available_nodes:
            logger.info(f"Using IOTA Node: {available_nodes[0]}")
            api_entry = iota.Iota(available_nodes[0])
        else:
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
