from app import db
from datetime import datetime

class PrivacySettings(db.Model):
    __tablename__ = 'privacy_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    personal_info_visibility = db.Column(db.String(20), default='private')   # 'private', 'friends', 'public'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 与User模型关联
    user = db.relationship('User', backref=db.backref('privacy_settings', lazy=True))

    def to_dict(self):
        return {
            'personalInfoVisibility': self.personal_info_visibility
        }