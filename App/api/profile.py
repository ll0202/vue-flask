import base64
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from App.models.user import db, User


api = Blueprint('profile', __name__, url_prefix='')
api_restful = Api(api)

class Find(Resource):
    def get(self):
        # 获取用户名参数
        username = request.args.get('username')  # 获取前端传递的用户名
        print("Current URL:", request.url)  # 打印当前 URL
        print("Username:", username)  # 打印传递的用户名

        # 查询用户信息
        user = User.query.filter_by(username=username).first()
        print(user.id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        photo_base64 = None
        if user.photo:
            photo_base64 = base64.b64encode(user.photo).decode('utf-8')  # 转换为 Base64 字符串

        # 返回用户信息，包括头像
        return jsonify({
            "id": user.id,
            "password": user.password,  # 如果密码加密过，不建议返回
            "username": user.username,
            "email": user.email,
            "photo": photo_base64  # 返回头像的 Base64 编码
        })



class Save(Resource):
    def post(self):
        if request.content_type.startswith('multipart/form-data'):
            userid = request.form.get('userid')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            file = request.files.get('avatar')

            print(f"Received userid: {userid}")
            print(f"Received username: {username}")
            print(f"Received email: {email}")
            print(f"Received password: {password}")
            print(f"Received file: {file}")

        user = User.query.filter_by(id=userid).first()
        if not user:
            return jsonify({"message": "User not found"})

        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = password  # 应使用加密函数处理
        if file:
            # 保存文件的二进制内容，确保处理文件保存逻辑
            user.photo = file.read()

        db.session.commit()

        print("Current URL:", request.url)
        print("Username:", username)

        return jsonify({"message": "个人信息修改成功",
                        'username': user.username
                        })
# 添加 Profile 资源并设置路由
api_restful.add_resource(Save, '/save')
api_restful.add_resource(Find, '/find')



# class Save(Resource):
#     def post(self):
#         # 获取请求数据
#         data = request.get_json()
#         userid = data['userid']
#         username = data.get('username')  # 用户名
#         email = data.get('email')  # 电子邮件
#         password = data.get('password')  # 密码
#         file = request.files.get('avatar')
#
#         print(file)
#         # 查询用户
#         user = User.query.filter_by(id=userid).first()
#         if not user:
#             return jsonify({"message": "User not found"}), 404
#
#         # 更新用户信息
#         if username:
#             user.username = username
#         if email:
#             user.email = email
#         if password:
#             user.password = password  # 假设密码需要加密，这里应该使用加密函数处理密码、
#         if file:
#             user.photo = file.read()
#
#         db.session.commit()  # 提交更改
#
#         print("Current URL:", request.url)  # 打印当前 URL
#         print("Username :", username)  # 打印传递的用户名
#
#         return jsonify({"message": "个人信息修改成功"})
#
# # # 添加 Profile 资源并设置路由
#
# api_restful.add_resource(Save, '/save')
