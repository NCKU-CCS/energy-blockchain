from flask import Flask
# from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Cryptodome.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Cryptodome.PublicKey import RSA

app = Flask(__name__)
app.config.from_pyfile('config.py')

# # random
# random_generator = Random.new().read

# encrypt
plat_rsa_pub_key = RSA.importKey(open('rsa/plat_rsa_public.pem').read())
ami_cipher = Cipher_pkcs1_v1_5.new(plat_rsa_pub_key)

# signature
ami_rsa_pub_key = RSA.importKey(open('rsa/ami_rsa_private.pem').read())
ami_signer = Signature_pkcs1_v1_5.new(ami_rsa_pub_key)