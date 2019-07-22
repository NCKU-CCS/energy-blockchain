from flask import Flask
from flask_restful import Api
from resources.hems import Hems
from resources.bems import Bems
from resources.get_transaction import Get_transaction
from config import app

api = Api(app)
# Hems
api.add_resource(Hems, "/hems/<string:name>")

# Bems
api.add_resource(Bems, "/bems/<string:name>")

# Get Transaction
api.add_resource(Get_transaction, "/get_transaction/<string:name>")

if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug='no')
