import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, send_from_directory, make_response    # 用于创建Flask应用实例和返回JSON响应
from flask_sqlalchemy import SQLAlchemy   # 用于ORM(对象关系映射)操作数据库
from flask_cors import CORS   # 用于处理跨域请求（允许前端访问后端API）
from flask_jwt_extended import JWTManager   # 用于JWT认证(保护需要登录的接口)
from flask_compress import Compress   # ✅ 用于gzip压缩
from config import Config   # 用于加载应用配置（如数据库连接信息）
from app.utils.error_handlers import APIError
from flask_mail import Mail
import os
import mimetypes

# 获取项目根目录绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(BASE_DIR, 'app.log'), encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

# 初始化扩展
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
compress = Compress()  # ✅ 初始化压缩扩展

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 配置日志
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 移除重复的处理器
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 文件处理器（带轮转）
    file_handler = RotatingFileHandler(
        os.path.join(BASE_DIR, 'app.log'),
        maxBytes=1024 * 1024 * 10,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)

    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # 初始化扩展
    db.init_app(app)    # 初始化SQLAlchemy扩展，将应用实例绑定到数据库会话
    jwt.init_app(app)    # 初始化JWTManager扩展，将应用实例绑定到JWT令牌的生成和验证
    CORS(app)    # 允许跨域请求
    compress.init_app(app)    # ✅ 启用gzip压缩

    # 邮箱配置（放在create_app函数内部）
    app.config['MAIL_SERVER'] = 'smtp.163.com'   # SMTP服务器地址
    app.config['MAIL_PORT'] = 465               # SSL端口
    app.config['MAIL_USE_SSL'] = True           # 使用SSL加密
    app.config['MAIL_USERNAME'] = 'xiaoqinghe_verify@163.com'   # 发送邮件的邮箱
    app.config['MAIL_PASSWORD'] = 'PUXuj3PRqGXvWdmd'      # 邮箱授权码（不是登录密码）
    app.config['MAIL_DEFAULT_SENDER'] = 'xiaoqinghe_verify@163.com'  # 默认发件人

    # 初始化邮件扩展
    mail.init_app(app)

    # 配置文件上传路径（服务器端路径）
    app.config['UPLOAD_FOLDER'] = '/var/www/uploads/'
    # 限制上传的文件大小为16MB
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # 创建上传目录（如果不存在）
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # 注册路由
    from app.routes.auth import auth_bp
    from app.routes.feedback import feedback_bp
    from app.routes.version import version_bp
    from app.routes.countdown import countdown_bp
    from app.routes.captcha import captcha_bp
    from app.routes.verify_code import verify_code_bp
    from app.routes.notification import notification_bp
    from app.routes.device import device_bp
    from app.routes.privacy import privacy_bp
    from app.routes.user_notification_setting import notification_setting_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(feedback_bp, url_prefix='/api/feedback')
    app.register_blueprint(version_bp, url_prefix='/api/version')
    app.register_blueprint(countdown_bp, url_prefix='/api/countdown')
    app.register_blueprint(captcha_bp, url_prefix='/api')
    app.register_blueprint(verify_code_bp, url_prefix='/api/verify')
    app.register_blueprint(notification_bp, url_prefix='/api/notification')
    app.register_blueprint(device_bp, url_prefix='/api/devices')
    app.register_blueprint(privacy_bp, url_prefix='/api/privacy')
    app.register_blueprint(notification_setting_bp, url_prefix='/api/notification/settings')

    # 创建数据库表（在MySQL中生成表结构）
    with app.app_context():       # 进入Flask应用的上下文环境。Flask的很多操作（如数据库操作）需要在应用上下文中执行
        from app.models.user_notification_setting import UserNotificationSetting
        db.create_all()    # 根据models中定义的模型，在MySQL中生成对应的表结构（如user表和feedback表）
        logger.info('数据库表创建成功')

    # 注册错误处理器
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify({'message': error.message})
        response.status_code = error.status_code
        return response 

    @app.errorhandler(500)
    def handle_internal_error(error):
        return jsonify({'message': '服务器内部错误'}), 500
    
    # JWT 错误处理
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        logger.error(f'JWT token 过期: {jwt_payload}')
        return jsonify({'message': '登录已过期，请重新登录'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        logger.error(f'JWT token 无效: {error}')
        return jsonify({'message': '无效的登录凭证'}), 422
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        logger.error(f'未授权访问: {error}')
        return jsonify({'message': '请先登录'}), 401
    
    # 配置静态文件服务（让前端可以访问上传的图片）
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        # 确保上传目录存在
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        # 记录访问日志，方便调试
        logger.info(f'访问上传文件: {filename}')
        logger.info(f'上传目录: {app.config["UPLOAD_FOLDER"]}')
        
        try:
            response = make_response(send_from_directory(app.config['UPLOAD_FOLDER'], filename))
            # ✅ 添加缓存头：图片资源缓存1年
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
                response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
            elif ext in ['.js', '.css']:
                response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
            else:
                response.headers['Cache-Control'] = 'public, max-age=86400'
            return response
        except Exception as e:
            logger.error(f'访问上传文件失败: {filename}, 错误: {str(e)}')
            return jsonify({'message': '文件不存在'}), 404
    
    # 处理文件过大的错误
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({'message': '上传文件大小超过限制（最大16MB）'}), 413

    return app    # 返回创建好的Flask应用实例，供run.py文件启动使用