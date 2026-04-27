from app import db
from passlib.hash import pbkdf2_sha256 as sha256
import logging
from datetime import datetime 

logger = logging.getLogger(__name__)

class User(db.Model):
    # 表名（默认会将类名转为小写作为表名，这里显示指定）
    __tablename__ = 'user'

    # 字段定义
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)   # 主键，自增
    username = db.Column(db.String(50), unique = True, nullable = False)   # 用户名，唯一，非空
    email = db.Column(db.String(120), unique = True, nullable = False)     # 邮箱，唯一，非空
    password_hash = db.Column(db.String(128), nullable = False)    # 密码（哈希存储）
    phone = db.Column(db.String(20), nullable = True)   # 手机号，可选
    avatar = db.Column(db.String(255), nullable = True)     # 头像URL,可选
    nickname = db.Column(db.String(50), nullable=True)      # 昵称，可选
    created_at = db.Column(db.DateTime, default = datetime.utcnow)    # 创建时间，默认当前时间

    # 密码哈希方式
    def set_password(self, password):
        self.password_hash = sha256.hash(password)

    # 密码验证方法
    def check_password(self, password):
        return sha256.verify(password, self.password_hash)