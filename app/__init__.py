from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from config import config
from app.extensions import bootstrap, db, login_manager, mail, moment
# from flask_apscheduler import APScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
import pymysql
from .api import api as api_blueprint

pymysql.install_as_MySQLdb()
# scheduler = APScheduler(scheduler=BackgroundScheduler(timezone="Asia/Shanghai"))


def create_app(config_name="development"):
    app = Flask(__name__)

    # 引入配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 注册扩展
    register_extensions(app)
    register_blueprints(app)

    return app


# 注册扩展
def register_extensions(app):
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    db.init_app(app)


# 注册蓝图
def register_blueprints(app):
    app.register_blueprint(api_blueprint, url_prefix='/api')