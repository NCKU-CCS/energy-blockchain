from flask import Flask
from flask_restful import Api
from resources.cems import Cems
from resources.bems import Bems
from resources.get_transaction import Get_transaction
from config import app

api = Api(app)
# Cems
api.add_resource(Cems, "/cems/<string:name>")

# Bems
api.add_resource(Bems, "/bems/<string:name>")

# Get Transaction
api.add_resource(Get_transaction, "/get_transaction/<string:tx_hash>")

if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug='no')
