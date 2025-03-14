from flask import Flask
import endpoints

api = Flask(__name__)
api.register_blueprint(endpoints.nfc_chip.blueprint)


if __name__ == "__main__":
    api.run("0.0.0.0", 5000)