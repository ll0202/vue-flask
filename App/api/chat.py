
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource


from App.models.user import Chat_models, ChatHistory, ChatMessage, db
from App.util.chat_demo import ChatBot

api = Blueprint('chat', __name__, url_prefix='')
api_restful = Api(api)

APPID = None
APISecret = None
APIKey = None
APIURL = None

class Chat_keys_select(Resource):
    def post(self):
        data = request.get_json()
        keyname = data.get('keyname')  # 获取模型名
        global APPID, APISecret, APIKey, APIURL
        # 查询数据库，获取对应模型的 APPID 和 APIKey
        chat_model = Chat_models.query.filter_by(name=keyname).first()
        if chat_model:
            APPID, APISecret, APIKey = chat_model.value.split('-')
            APIURL = chat_model.url

            print(APPID, APISecret, APIKey, APIURL)

            return jsonify({
                "status": "success",
                "message": f"模型 {keyname} 已选择并缓存",
            })
        else:
            return jsonify({
                "status": "error",
                "message": "未找到对应的模型"
            }), 404



class SendMessage(Resource):
    def post(self):
        # 获取前端发送的JSON数据
        data = request.get_json()
        user_message = data.get('message', '你好')  # 默认消息是“你好”
        print("用户消息:", user_message)

        # 从全局变量获取API密钥等信息
        global APPID, APISecret, APIKey, APIURL
        app_id = APPID
        api_key = APIKey
        api_secret = APISecret
        api_url = APIURL

        # 如果没有配置必要的API信息，返回错误
        if not app_id or not api_key or not api_secret:
            return jsonify({
                "status": "error",
                "message": "未选择模型，请先选择模型"
            })
        try:
            # 创建ChatBot实例并生成模型的响应
            chat = ChatBot(
                appid=app_id,
                api_key=api_key,
                api_secret=api_secret,
                Spark_url=api_url,
                domain='generalv3.5'
            )
            # 调用ChatBot实例获取响应
            response = chat.ask_question(user_message)
            print('模型返回的响应:', response)

            # 将响应包装成字典格式，并返回给前端
            return jsonify({
                "status": 1,
                "response": response
            })
        except Exception as e:
            # 其他异常处理
            return jsonify({
                "status": "error",
                "message": str(e)
            })



class Message(Resource):
    def post(self):
        # 从请求中获取 JSON 数据
        data = request.get_json()
        print("接收到的数据:", data)  # 打印接收到的完整数据

        # 根据需要解析数据中的字段
        messages = data.get('messages', [])
        news = data.get('news', [])
        username = data.get('username', 'anonymous')
        print("username:", username)
        print("消息列表:", messages)
        print("新闻数据:", news)

        # 存储新闻数据到 ChatHistory 表
        if news:
            news_content = news[-1]['content']
            new_chat_history = ChatHistory(user_name=username, title=news_content)  # 确保字段名与模型匹配
            db.session.add(new_chat_history)
            db.session.commit()  # 提交事务以生成id

            # 存储消息列表数据到 ChatMessage 表
            for message in messages:
                new_chat_message = ChatMessage(chat_history_id=new_chat_history.id, message=message['content'], sender=message['role'])
                db.session.add(new_chat_message)
            db.session.commit()  # 提交事务

        # 返回固定的响应
        return jsonify({
            "status": new_chat_history.id,
            "message": "数据已接收并存储",
        })


class History_messages(Resource):
    def get(self):
        # 从请求的参数中获取 chat_history_id
        chat_history_id = request.args.get('news_ID')
        print("chat-history_id:", chat_history_id)

        # 如果没有提供 chat_history_id，返回错误响应
        if not chat_history_id:
            return {"message": "Missing chat_history_id parameter"}, 400

        # 查询 chat_message 表，获取对应的历史消息
        try:
            # 查询数据库，获取历史消息
            chat_messages = ChatMessage.query.filter_by(chat_history_id=chat_history_id).all()

            # 如果没有找到任何消息，返回空列表
            if not chat_messages:
                return {"message": "No messages found for this chat history ID"}

            # 将消息转换为字典格式返回给前端
            messages = []
            for message in chat_messages:
                messages.append({
                    "message": message.message,  # 使用 message 字段
                    "sender": message.sender,    # 使用 sender 字段
                })

            # 返回找到的消息
            return jsonify(messages)

        except Exception as e:
            # 捕获任何异常并返回 500 错误
            return {"message": str(e)}

class Delete_Chat_message(Resource):
    def get(self):
        chat_history_id = request.args.get('news_ID')
        print("chat-history_id:", chat_history_id)

        # 首先，删除所有相关的 ChatMessage 记录
        chat_messages = ChatMessage.query.filter_by(chat_history_id=chat_history_id).all()
        print("ChatMessages to be deleted:", chat_messages)
        for message in chat_messages:
            db.session.delete(message)
        db.session.commit()  # 删除完消息后提交事务

        # 然后，删除对应的 ChatHistory 记录
        chat_history = ChatHistory.query.get(chat_history_id)
        if chat_history:
            db.session.delete(chat_history)
            db.session.commit()  # 提交删除 ChatHistory 记录的事务
            return {'message': 'Chat history and messages deleted successfully', 'status': 1}
        else:
            return {'message': 'Chat history not found'}

api_restful.add_resource(Chat_keys_select, '/keyselect')
api_restful.add_resource(SendMessage, '/sendmessage')
api_restful.add_resource(Message, '/save')  # 新增路由
api_restful.add_resource(History_messages, '/messages')
api_restful.add_resource(Delete_Chat_message, '/delect/message')

