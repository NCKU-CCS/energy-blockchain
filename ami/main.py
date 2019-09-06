from flask import Flask
from flask_restful import Api
from resources.bems import Bems
from config import app

api = Api(app)

# Bems
api.add_resource(Bems, "/bems/upload")

if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug='no', ssl_context=app.config['SSL_CONTEXT'])
