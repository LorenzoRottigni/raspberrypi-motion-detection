# app/__init__.py
from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Ensure this path is correct
    print(app.config)
    app.register_blueprint(main)
    return app
