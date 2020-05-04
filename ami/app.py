from flask import Flask
from flask_restful import Api
from resources.bems import Bems


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("./config/config.py")
    api = Api(app)
    api.add_resource(Bems, "/bems/upload")
    return app


def main():
    app = create_app()
    app.run(host=app.config["HOST"], port=app.config["PORT"], threaded=True)


if __name__ == "__main__":
    main()
