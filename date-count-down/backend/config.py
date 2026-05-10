import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'e7c3640ebf0f26a1fc46c1fa0b59be96')
    # MySQL连接字符串：mysql+pymysql://用户名:密码@主机:端口/数据库名
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:20051021@localhost:3306/countdown_app')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'e7c3640ebf0f26a1fc46c1fa0b59be96')
    
    # 数据库连接池配置
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,  # 增加连接池大小
        'max_overflow': 50,  # 增加溢出连接数
        'pool_timeout': 60,  # 增加超时时间
        'pool_recycle': 300,  # 5分钟回收连接
        'echo': False  # 关闭SQL日志输出
    }