import os

from dotenv import load_dotenv

load_dotenv()


BEMS_ACCEPT = [
    "bems_homepage_information",
    "bems_ess_display",
    "bems_ev_display",
    "bems_pv_display",
    "bems_wt_display",
]

API_TX = os.environ.get("API_TX", "http://140.116.247.120:5000/address")

TOKEN = {
    "Carlab_BEMS": os.environ.get("TOKEN_CARLAB_BEMS"),
    "SGESC_C_BEMS": os.environ.get("TOKEN_SGESC_C_BEMS"),
    "SGESC_D_BEMS": os.environ.get("TOKEN_SGESC_D_BEMS"),
    "ABRI_BEMS": os.environ.get("TOKEN_ABRI_BEMS"),
}

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 4000)

ALLOWED_IPS = os.environ.get("ALLOWED_IPS", "127.0.0.1").split(",")
