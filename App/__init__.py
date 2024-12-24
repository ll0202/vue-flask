from flask import Flask
from flask_cors import CORS
from App.models.user import db
from App.api.login import api
from App.config import config
from App.util.urls import register_blueprints


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    CORS(app)
    register_blueprints(app)

    # # 注册蓝图
    # app.register_blueprint（API）

    print("Registered routes:", app.url_map)
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