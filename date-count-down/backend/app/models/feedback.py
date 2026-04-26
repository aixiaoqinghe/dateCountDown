from app import db
from datetime import datetime

class Feedback(db.Model):
    # 表名
    __tablename__ = 'feedback'

    # 字段定义
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)    # 主键，自增
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)    # 外键关联user表
    rating = db.Column(db.Integer, nullable = False)    # 评分（1-5星）
    feedback_type = db.Column(db.String(50), nullable = False)    # 反馈类型（如“功能建议”）
    content = db.Column(db.Text, nullable = False)   # 反馈内容
    created_at = db.Column(db.DateTime, default = datetime.utcnow)    # 创建时间
    