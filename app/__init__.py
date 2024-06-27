from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import logging

from models.userModel import db
from logger.log import log
from flask_mail import Mail
from utils.config import settings
mail = Mail()

def create_app():
    app = Flask(__name__)
    ma = Marshmallow(app)

    app = Flask(__name__)

    # Configure Flask-Mail
    app.config['MAIL_SERVER'] = settings['mail']['server']
    app.config['MAIL_PORT'] = settings['mail']['port']
    app.config['MAIL_USE_TLS'] = settings['mail']['use_tls']
    app.config['MAIL_USERNAME'] = settings['mail']['username']
    app.config['MAIL_PASSWORD'] = settings['mail']['password']

    mail.init_app(app)

    default_log = logging.getLogger('werkzeug')
    default_log.setLevel(logging.ERROR)

    # applies CORS headers to all routes, enabling resources to be accessed
    CORS(app, origins="*")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/python'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False

    migrate = Migrate(app, db)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    from routers.index import api_bp

    app.register_blueprint(api_bp, url_prefix='/api')

    return app

