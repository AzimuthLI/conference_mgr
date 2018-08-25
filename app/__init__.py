from flask_api import FlaskAPI
from instance.config import app_config
from app.db import db
import sys, os

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app import auth
    app.register_blueprint(auth.bp)

    from app import conference_manage
    app.register_blueprint(conference_manage.bp)
    # app.add_url_rule('/', endpoint='index')

    return app