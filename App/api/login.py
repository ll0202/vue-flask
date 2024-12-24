import base64
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from App.models.user import db, User

# api = Blueprint('api', __name__, , url_prefix='')
# api_restful = Api(api)

api = Blueprint('api', __name__, url_prefix='')
api_restful = Api(api)

class Register(Resource):
    def post(self):
        # 获取请求数据
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # 检查是否提供了所有必要的数据
        if not username or not email or not password:
            return jsonify({'status': 'fail', 'message': '缺少必要的字段'})

        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({'status': 'fail', 'message': '用户名已存在'})

        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            return jsonify({'status': 'fail', 'message': '邮箱已被注册'})

        try:
            # 打印调试信息
            print(f"Registering user: {username}, {email}")

            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'status': 'success', 'message': '注册成功'})
        except Exception as e:
            db.session.rollback()
            print(f"Error during registration: {e}")  # 打印错误信息
            return jsonify({'status': 'fail', 'message': f'注册失败: {str(e)}'})


class Login(Resource):
    def post(self):
        # 获取请求数据
        data = request.get_json()
        username = data.get('userName')
        password = data.get('passWord')

        # 查询用户信息
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'status': 3, 'message': '该用户名暂未注册'})

        # 验证密码
        if user.password == password:
            token = "mocked_token_for_demo"  # 模拟 token

            # 将头像的二进制数据转换为 Base64
            photo_base64 = None
            if user.photo:  # 假设 photo 是保存头像二进制的字段
                photo_base64 = base64.b64encode(user.photo).decode('utf-8')

            return jsonify({
                'status': 1,
                'message': '登录成功',
                'token': token,
                'username': user.username,
                'photo': photo_base64  # 返回 Base64 编码的头像
            })
        else:
            return jsonify({'status': 2, 'message': '密码错误'})

# 添加资源到 API 路由
api_restful.add_resource(Register, '/register')
api_restful.add_resource(Login, '/login')


