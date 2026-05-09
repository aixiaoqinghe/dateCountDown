# backend/app/models/user_notification_setting.py

from app import db
from datetime import datetime

class UserNotificationSetting(db.Model):
    __tablename__ = 'user_notification_settings'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    countdown_reminder = db.Column(db.Boolean, default=True)
    system_messages = db.Column(db.Boolean, default=True)
    activity_notifications = db.Column(db.Boolean, default=True)
    important_notifications = db.Column(db.Boolean, default=True) # 通常不允许关闭
    popup_notification = db.Column(db.Boolean, default=True)
    sound_notification = db.Column(db.Boolean, default=True)
    vibration_notification = db.Column(db.Boolean, default=True)
    notification_frequency = db.Column(db.String(20), default='realtime')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联用户
    user = db.relationship('User', backref=db.backref('notification_setting', uselist=False))

    def to_dict(self):
        return {
            'countdownReminder': self.countdown_reminder,
            'systemMessages': self.system_messages,
            'activityNotifications': self.activity_notifications,
            'importantNotifications': self.important_notifications,
            'popupNotification': self.popup_notification,
            'soundNotification': self.sound_notification,
            'vibrationNotification': self.vibration_notification,
            'notificationFrequency': self.notification_frequency,
        }
