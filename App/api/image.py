import base64
from flask import Blueprint, request, jsonify, send_file
from flask_restful import Api, Resource
from App.models.user import Chat_models
import os
from App.util.image_demo import base64_to_image, main  # 你已经写好的生成图片和保存的函数
from PIL import Image
import json

api = Blueprint('image', __name__, url_prefix='')
api_restful = Api(api)

APPID = None
APISecret = None
APIKey = None
APIURL = None


class Image_keys_select(Resource):
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
            })

class Image_send(Resource):
    def post(self):
        data = request.get_json()
        description = data['description']
        width = data['width']
        height = data['height']

        global APPID, APISecret, APIKey

        # 调用外部 API 生成图片
        response = main(description, width, height, APPID, APIKey, APISecret)

        # 解析并保存图片
        save_path, image_base64 = self.save_image_from_response(response)

        if save_path:
            # 返回图片的 base64 格式，或图片路径（根据需求）
            return jsonify({
                "status": 1,
                "message": "图片生成成功",
                "image_base64": image_base64,  # 返回 Base64 图片
                "image_path": save_path  # 可选：返回图片路径
            })
        else:
            return jsonify({
                "status": 2,
                "message": "图片生成失败"
            })

    def save_image_from_response(self, response):
        try:
            # 解析返回的 JSON 数据，提取图片的 base64 内容
            data = json.loads(response)
            code = data['header']['code']
            if code != 0:
                print(f"请求错误: {code}, {data}")
                return None, None

            # 提取图片的 base64 数据
            image_content = data["payload"]["choices"]["text"][0]
            image_base = image_content["content"]

            # 生成保存图片的文件路径
            image_name = data['header']['sid']
            save_path = f"static/uploads/{image_name}.jpg"

            # 保存图片到本地
            base64_to_image(image_base, save_path)

            # 返回图片路径和 base64 数据
            image_base64 = self.convert_image_to_base64(save_path)
            return save_path, image_base64

        except Exception as e:
            print(f"图片解析或保存失败: {str(e)}")
            return None, None

    def convert_image_to_base64(self, image_path):
        """将图片文件转换为 base64 格式"""
        try:
            with open(image_path, "rb") as img_file:
                # 读取图片并转换为base64
                image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            return image_base64
        except Exception as e:
            print(f"图片转换为Base64失败: {str(e)}")
            return None

def base64_to_image(base64_data, file_path):
    """将Base64编码的图片数据保存为图片文件"""
    try:
        # 去掉 Base64 数据的头部（如果存在的话）
        if base64_data.startswith('data:image/jpeg;base64,'):
            base64_data = base64_data.split('base64,')[1]

        # 将Base64数据解码为二进制
        img_data = base64.b64decode(base64_data)

        # 保存图片
        with open(file_path, 'wb') as f:
            f.write(img_data)

        return True
    except Exception as e:
        print(f"保存图片失败: {str(e)}")
        return False


api_restful.add_resource(Image_send, '/send')  # 新增路由
api_restful.add_resource(Image_keys_select, '/keys')
