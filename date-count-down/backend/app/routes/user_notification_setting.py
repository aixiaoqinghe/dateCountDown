# backend/app/routes/user_notification_setting.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user_notification_setting import UserNotificationSetting
import logging

notification_setting_bp = Blueprint('notification_setting', __name__)
logger = logging.getLogger(__name__)

# 获取用户通知设置
@notification_setting_bp.route('', methods=['GET'])
@jwt_required()
def get_notification_setting():
    user_id = int(get_jwt_identity())

    # 尝试获取现有设置
    setting = UserNotificationSetting.query.filter_by(user_id=user_id).first()

    if setting:
        logger.info(f"获取用户 {user_id} 的通知设置")
        return jsonify(setting.to_dict()), 200
    else:
        # 如果没有设置，返回默认值
        default_setting = {
            'countdownReminder': True,
            'systemMessages': True,
            'activityNotifications': True,
            'importantNotifications': True,
            'popupNotification': True,
            'soundNotification': True,
            'vibrationNotification': True,
            'notificationFrequency': 'realtime',
        }
        return jsonify(default_setting), 200
    
# 更新用户通知设置
@notification_setting_bp.route('', methods=['PUT'])
@jwt_required()
def update_notification_setting():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    # 尝试获取现有设置
    setting = UserNotificationSetting.query.filter_by(user_id=user_id).first()

    if not setting:
        # 如果没有设置，创建新的
        setting = UserNotificationSetting(user_id=user_id)

    # 更新字段（只更新请求中包含的字段）
    if 'countdownReminder' in data:
        setting.countdown_reminder = data['countdownReminder']
    if 'systemMessages' in data: 
        setting.system_messages = data['systemMessages']
    if 'activityNotifications' in data:
        setting.activity_notifications = data['activityNotifications']
    # important_notifications 通常不允许用户修改，保持默认True
    if 'popupNotification' in data:
        setting.popup_notification = data['popupNotification']
    if 'soundNotification' in data:
        setting.sound_notification = data['soundNotification']
    if 'vibrationNotification' in data:
        setting.vibration_notification = data['vibrationNotification']
    if 'notificationFrequency' in data:
        setting.notification_frequency = data['notificationFrequency']

    db.session.add(setting)
    db.session.commit()

    return jsonify({'message': '通知设置更新成功', 'data': setting.to_dict()}), 200
