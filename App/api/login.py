from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from App.models.user import db, User

# 创建 Blueprint 和 Api 实例
api = Blueprint('api', __name__)
api_restful = Api(api)

class Login(Resource):
    def post(self):
        # 获取请求数据
        data = request.get_json()
        username = data.get('userName')  # 修改字段名为 userName
        password = data.get('passWord')  # 修改字段名为 passWord

        # 查询用户信息
        user = User.query.filter_by(username=username).first()
        if not user:
            # 如果用户不存在
            return jsonify({'status': 3, 'message': '该用户名暂未注册'})

        # 验证密码（不加密）
        if user.password == password:
            # 假设后端生成并返回 token
            token = "mocked_token_for_demo"  # 实际中应生成 JWT 或其他安全 token
            return jsonify({'status': 1, 'message': '登录成功', 'token': token})
        else:
            return jsonify({'status': 2, 'message': '密码错误'})

# 添加资源到 API 路由
api_restful.add_resource(Login, '/api/login')