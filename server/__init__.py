from flask import Flask
from .routes import main
from os import getenv
from .config import Config  # Make sure this import works correctly

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Ensure this path is correct
    app.register_blueprint(main)
    return app

app = create_app()

if __name__ == '__main__':
    from waitress import serve
    serve(
        app,
        host=getenv("FLASK_HOST", "127.0.0.1"),  # Default to localhost if FLASK_HOST is not set
        port=int(getenv("FLASK_PORT", 5000))  # Default to port 5000 if FLASK_PORT is not set
    )
