from datetime import datetime
from app import db

class Device(db.Model):
    __tablename__ = 'device'

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    device_id = db.Column(db.String(100), unique=True, nullable = False)   # 设备唯一标识
    name = db.Column(db.String(100))   # 设备名称（前端用 name）
    device_type = db.Column(db.String(10))  # 设备类型（前端用deviceType）
    os = db.Column(db.String(100))  # 操作系统
    browser = db.Column(db.String(100))   # 浏览器
    location = db.Column(db.String(100))   # 位置
    ip = db.Column(db.String(50))    # IP地址
    last_login = db.Column(db.DateTime, default = datetime.utcnow)   # 最后登录时间
    created_at = db.Column(db.DateTime, default = datetime.utcnow)   # 创建时间

    # 关联用户
    user = db.relationship('User', backref=db.backref('devices', lazy=True))

    # 转换为前端需要的格式
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'device_type': self.device_type,   # 前端用camelCase
            'os': self.os,
            'browser': self.browser,
            'location': self.location,
            'ip': self.ip,
            'lastLogin': self.last_login.strftime('%Y-%m-%d %H:%M:%S'),  # 前端用camelCase
            'isCurrent': False   # 默认不是当前设备，后续动态设置
        }