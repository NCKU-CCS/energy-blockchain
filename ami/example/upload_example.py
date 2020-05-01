import uuid
from datetime import datetime
import random

import requests
from loguru import logger


API_TX = "http://127.0.0.1:4000/bems/upload"
AMIS = ["Carlab_BEMS", "SGESC_C_BEMS", "SGESC_D_BEMS", "ABRI_BEMS"]


def generate_detail(field):
    pv = float("%.3f" % random.uniform(-5, 5))
    ess = float("%.3f" % random.uniform(-5, 5))
    ev = float("%.3f" % random.uniform(-5, 5))
    building = float("%.3f" % random.uniform(-1, 5))
    grid = float("%.3f" % (pv + ess + ev + building + random.uniform(-1, 1)))
    data_type = {
        "bems_homepage_information": {
            "id": str(uuid.uuid4()),
            "field": field,
            "grid": grid,
            "pv": pv,
            "building": building,
            "ess": ess,
            "ev": ev,
            "updated_at": datetime.today().isoformat(),
        },
        "bems_ess_display": {
            "id": str(uuid.uuid4()),
            "field": field,
            "cluster": 1,
            "power_display": ess,
            "updated_at": datetime.today().isoformat(),
        },
        "bems_ev_display": {
            "id": str(uuid.uuid4()),
            "field": field,
            "cluster": 1,
            "power": ev,
            "updated_at": datetime.today().isoformat(),
        },
        "bems_pv_display": {
            "id": str(uuid.uuid4()),
            "field": field,
            "cluster": 1,
            "PAC": pv,
            "updated_at": datetime.today().isoformat(),
        },
        "bems_wt_display": {
            "id": str(uuid.uuid4()),
            "field": field,
            "cluster": 1,
            "WindGridPower": float("%.3f" % random.uniform(-5, 5)),
            "updated_at": datetime.today().isoformat(),
        },
    }
    return data_type


def generate_data():
    data = {}
    for ami in AMIS:
        data[ami] = generate_detail(ami)
    return data


def main():
    data = generate_data()
    response = requests.post(API_TX, json=data)
    logger.info(response.text)


if __name__ == "__main__":
    main()
