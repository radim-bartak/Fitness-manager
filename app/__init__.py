from flask import Flask, render_template
from app.models import db
from app.routes.members import members_bp
from app.routes.trainers import trainers_bp
from app.routes.classes import classes_bp
from app.routes.reservation import reservation_bp
from app.config import Config, ConfigError

def create_app():
    app = Flask(__name__)

    try:
        config = Config("config.json")
        app.config["SQLALCHEMY_DATABASE_URI"] = config.get_database_uri()
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    except ConfigError as e:
        print(f"Configuration error: {e}")
        exit(1)

    db.init_app(app)

    app.register_blueprint(members_bp, url_prefix='/')
    app.register_blueprint(trainers_bp, url_prefix='/')
    app.register_blueprint(classes_bp, url_prefix='/')
    app.register_blueprint(reservation_bp, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app