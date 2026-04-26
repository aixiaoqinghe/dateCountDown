import logging
from flask import Flask    # 用于创建Flask应用实例
from flask_sqlalchemy import SQLAlchemy   # 用于ORM(对象关系映射)操作数据库
from flask_cors import CORS   # 用于处理跨域请求（允许前端访问后端API）
from flask_jwt_extended import JWTManager   # 用于JWT认证(保护需要登录的接口)
from config import Config   # 用于加载应用配置（如数据库连接信息）

# 配置日志
logging.basicConfig(
    level=logging.INFO,     # 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',   # 日志格式
    handlers=[
        logging.StreamHandler(),    # 输出到控制台
        logging.FileHandler('app.log')     # 输出到文件
    ]
)

logger = logging.getLogger(__name__)

# 初始化扩展
db = SQLAlchemy()    # 创建SQLAlchemy实例，后续用于数据库操作（如创建表、查询数据）
jwt = JWTManager()    # 创建JWTManager实例，后续用于JWT令牌的生成和验证

def create_app():
    app = Flask(__name__)   # 创建Flask应用实例，__name__用于确定应用的根目录（用于查找静态文件、模板等）
    app.config.from_object(Config)   # 加载Config类中的配置（如数据库连接字符串、密钥等）到应用实例中

    # 初始化扩展
    db.init_app(app)    # 初始化SQLAlchemy扩展，将应用实例绑定到数据库会话
    jwt.init_app(app)    # 初始化JWTManager扩展，将应用实例绑定到JWT令牌的生成和验证
    CORS(app)    # 允许跨域请求

    # 注册路由
    from app.routes.auth import auth_bp
    from app.routes.feedback import feedback_bp
    from app.routes.version import version_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(feedback_bp, url_prefix='/api/feedback')
    app.register_blueprint(version_bp, url_prefix = '/api/version')

    # 创建数据库表（在MySQL中生成表结构）
    with app.app_context():       # 进入Flask应用的上下文环境。Flask的很多操作（如数据库操作）需要在应用上下文中执行
        db.create_all()    # 根据models中定义的模型，在MySQL中生成对应的表结构（如user表和feedback表）
        logger.info('数据库表创建成功')

    return app    # 返回创建好的Flask应用实例，供run.py文件启动使用