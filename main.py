from flask import Flask
import endpoints

api = Flask(__name__)
api.register_blueprint(endpoints.nfc_chip.blueprint)


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=42590)  # Upraven pouze port