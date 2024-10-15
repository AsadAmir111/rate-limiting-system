from flask import Flask
from rate_limiting_system.endpoints import main

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app