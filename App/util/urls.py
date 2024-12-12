from flask import Flask
from App.api.login import api as login_api  # 导入登录蓝图

def register_blueprints(app: Flask):
    """
    注册所有蓝图
    """
    app.register_blueprint(login_api, url_prefix='/api')  # 注册蓝图
