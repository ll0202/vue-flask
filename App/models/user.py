from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, LargeBinary, ForeignKey

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)  # 与MySQL表中的name字段对应
    password = db.Column(db.String(200), nullable=False)
    photo = db.Column(db.LargeBinary) # 添加了photo字段
    email = db.Column(db.String(120), unique=True)

class Chat_models(db.Model):
    __tablename__ = 'chat_models'
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    value = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate="CASCADE"), nullable=False)


class ChatHistory(db.Model):
    __tablename__ = 'chathistory'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # 这里不需要显式定义外键，因为 SQLAlchemy 会自动处理

class ChatMessage(db.Model):
    __tablename__ = 'chatmessage'
    id = db.Column(db.Integer, primary_key=True)
    chat_history_id = db.Column(db.Integer, db.ForeignKey('chathistory.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # 可以添加一个 backref 来方便地从 ChatHistory 访问 ChatMessages
    chat_history = db.relationship('ChatHistory', backref=db.backref('messages', lazy=True))