from flask import Flask
from flask_cors import CORS
from App.models.user import db
from App.api.login import api
from App.config import config


def create_app(config_name='development'):
    app = Flask(__name__)

    # 加载通用配置
    app.config.from_object(config[config_name])

    # 加载实例级别的配置（如果存在）
    app.config.from_pyfile('config.py', silent=True)

    # 初始化数据库
    db.init_app(app)

    # 启用CORS
    CORS(app)

    # 注册蓝图
    app.register_blueprint(api)

    return app

#
# from flask import Flask
# from flask_cors import CORS
# from App.api.login import api
#
# def create_app():
#     app = Flask(__name__)
#     CORS(app)
#     app.register_blueprint(api)
#     return app