from datetime import datetime
from app import db
import logging

logger = logging.getLogger(__name__)

class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # 允许为NULL表示系统通知
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    message = db.Column(db.String(500))  # 简短消息，用于通知栏显示
    start_time = db.Column(db.DateTime)  # 通知开始时间
    end_time = db.Column(db.DateTime)    # 通知结束时间
    priority = db.Column(db.Integer, default=0)  # 优先级，数字越大优先级越高
    type = db.Column(db.String(20), default='info') # info, warning, success, error
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'message': self.message,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'priority': self.priority,
            'type': self.type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        }