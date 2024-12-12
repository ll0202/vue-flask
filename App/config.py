class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 其他通用配置

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/flask'



# 配置映射
config = {
    'development': DevelopmentConfig,

}
