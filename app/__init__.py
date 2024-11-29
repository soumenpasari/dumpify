from flask import Flask

def create_app():
    app = Flask(__name__)

    #registering the blueprint
    from .routes import main
    app.register_blueprint(main)
    return app