from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


    def __repr__(self):
        return f"<User(username={self.username}, id={self.id})>"
    #
    # def to_json(self):
    #     return {
    #         "id": self.id,
    #         "username": self.username,
    #         # 避免实际应用中直接返回密码
    #     }
