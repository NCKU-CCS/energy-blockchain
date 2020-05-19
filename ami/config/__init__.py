import os

from dotenv import load_dotenv
from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Cryptodome.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Cryptodome.PublicKey import RSA

load_dotenv()


API_URI = os.environ.get("API_URI", "https://nodes.thetangle.org:443").split(",")

API_OPEN = os.environ.get("API_OPEN", "https://nodes.thetangle.org:443")

# encrypt
PLAT_RSA_PUB_KEY = RSA.importKey(open("rsa/plat_rsa_public.pem").read())
AMI_CIPHER = Cipher_pkcs1_v1_5.new(PLAT_RSA_PUB_KEY)

# signature
AMI_RSA_PRI_KEY = RSA.importKey(open("rsa/ami_rsa_private.pem").read())
AMI_SIGNER = Signature_pkcs1_v1_5.new(AMI_RSA_PRI_KEY)
