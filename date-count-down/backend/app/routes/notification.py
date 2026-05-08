from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.notification import Notification
import logging

notification_bp = Blueprint('notification', __name__)
logger = logging.getLogger(__name__)

# 获取通知列表（包含系统通知和个人通知）
@notification_bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = int(get_jwt_identity())
    # 获取系统通知（user_id为NULL）和个人通知（user_id为当前用户）
    notifications = Notification.query.filter(
        (Notification.user_id == user_id) | (Notification.user_id.is_(None))
    ).order_by(Notification.priority.desc(), Notification.created_at.desc()).all()
    return jsonify([n.to_dict() for n in notifications]), 200

# 获取单个通知
@notification_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_notification(id):
    user_id = int(get_jwt_identity())
    notification = Notification.query.filter_by(id=id, user_id=user_id).first()
    if not notification:
        return jsonify({'message': '通知不存在'}), 404
    return jsonify(notification.to_dict()), 200

# 标记为已读
@notification_bp.route('/<int:id>/read', methods=['PUT'])
@jwt_required()
def mark_read(id):
    user_id = int(get_jwt_identity())
    notification = Notification.query.filter_by(id=id, user_id=user_id).first()
    if not notification:
        return jsonify({'message': '通知不存在'}), 404
    notification.is_read = True
    db.session.commit()
    return jsonify({'message': '通知已标记为已读'}), 200

# 删除通知
@notification_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_notification(id):
    user_id = int(get_jwt_identity())
    notification = Notification.query.filter_by(id=id, user_id=user_id).first()
    if not notification:
        return jsonify({'message': '通知不存在'}), 404
    db.session.delete(notification)
    db.session.commit()
    return jsonify({'message': '通知已删除'}), 200