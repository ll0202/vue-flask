from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from App.models.user import Chat_models, db, User

api = Blueprint('key', __name__, url_prefix='')
api_restful = Api(api)

class Key_save(Resource):
    def post(self):
        data = request.get_json()
        print("Received data:", data)
        platform = data.get('platform')
        name = data.get('name')
        url = data.get('url')
        val = data.get('val')
        username = data.get('username')
        type = data.get('type')
        print("Received username:", username)
        print(platform, name, url, val, type)

        user = User.query.filter_by(username=username).first()
        print("user value", user)
        if user is None:
            return jsonify({"status": "error", "message": "用户不存在"})

        # 创建一个新的 Chat_models 实例
        new_key = Chat_models(platform=platform, name=name, url=url, value=val, user_id=user.id, type=type)
        # 将实例添加到数据库会话中
        db.session.add(new_key)
        # 提交会话以保存到数据库
        db.session.commit()
        return jsonify({"status": "success", "message": "保存成功"})

class Key_delete(Resource):
    def post(self):
        data = request.get_json()
        print("Received data:", data)
        keyname = data.get('keyname')
        username = data.get('username')
        type = data.get('type')

        # 根据 keyname 查找记录
        key_to_delete = Chat_models.query.filter_by(name=keyname).first()
        if key_to_delete:
            try:
                # 删除记录
                db.session.delete(key_to_delete)
                db.session.commit()
                return jsonify({"status": 1,'message': 'Key deleted successfully'})
            except Exception as e:
                # 处理异常
                db.session.rollback()
                return jsonify({'error': str(e)})
        else:
            # 没有找到对应的记录
            return jsonify({'message': 'Key not found'})


api_restful.add_resource(Key_save, '/save')
api_restful.add_resource(Key_delete, '/delete')