from app import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Countdown(db.Model):
    __tablename__ = 'countdown'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    task_name = db.Column(db.String(100), nullable = False)
    target_date = db.Column(db.DateTime, nullable = False)
    category = db.Column(db.String(50), nullable = True)
    background_image = db.Column(db.Text(length=4294967295), nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)

    # 与user模型的关联
    user = db.relationship('User', backref = db.backref('countdowns', lazy = True))