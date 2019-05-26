from flask import Flask
from flask_restful import Api
from resources.hems import Hems
from resources.bems import Bems
from config import app

api = Api(app)
# Hems
api.add_resource(Hems, "/hems/<string:name>")

# Bems
api.add_resource(Bems, "/bems/<string:name>")

if __name__ == "__main__":
   app.run(host=app.config['HOST'], port=app.config['PORT'], debug='no')
