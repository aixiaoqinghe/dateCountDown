from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.notification import Notification
import logging

notification_bp = Blueprint('notification', __name__)
logger = logging.getLogger(__name__)

# 获取通知列表
@notification_bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = int(get_jwt_identity())
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
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
