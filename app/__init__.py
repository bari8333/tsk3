from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    # Register Blueprint with URL prefix
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')

    with app.app_context():
        from app import models
        db.create_all()

    return app