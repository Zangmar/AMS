from flask import Flask
from config import config
from config import global_config as gconfig
from lib.baiwangoa.model import db
from lib.baiwangoa.common.filter_define import filter_define


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # from obj attr to dict for config(importance)
    app.config['SQLALCHEMY_DATABASE_URI'] = gconfig.DB_LINK

    db.init_app(app)
    db.app = app

    from .api import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)
    from .admin import admin as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    from .hr import hr as hr_bp
    app.register_blueprint(hr_bp, url_prefix='/hr')
    from .employee import employee as employee_bp
    app.register_blueprint(employee_bp, url_prefix='/employee')

    # define filter
    filter_define(app)

    return app
