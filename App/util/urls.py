from flask import Flask
from App.api.login import api as login_api  # 导入登录蓝图
from App.api.profile import api as profile_api
from App.api.key import api as key_api
from App.api.chat import api as chat_api
from App.api.image import api as image_api

def register_blueprints(app: Flask):
    app.register_blueprint(login_api, url_prefix='/api')
    app.register_blueprint(profile_api, url_prefix='/api/profile')  # Ensure this line exists and is correct
    app.register_blueprint(key_api, url_prefix='/api/key')
    app.register_blueprint(chat_api, url_prefix='/api/chat')
    app.register_blueprint(image_api, url_prefix='/api/image')



