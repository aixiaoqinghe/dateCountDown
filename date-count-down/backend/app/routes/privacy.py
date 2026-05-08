from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.privacy import PrivacySettings
from app import db
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
privacy_bp = Blueprint('privacy', __name__)

# 获取隐私设置
@privacy_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_privacy_settings():
    logger.info('接收到获取隐私设置请求')
    user_id = int(get_jwt_identity())

    # 查找用户的隐私设置
    settings = PrivacySettings.query.filter_by(user_id=user_id).first()

    if settings:
        logger.info(f'找到用户{user_id}的隐私设置请求')
        return jsonify(settings.to_dict()), 200
    else:
        # 如果没有设置，返回默认设置
        logger.info(f'用户{user_id}没有隐私设置，返回默认值')
        return jsonify({
            'personalInfoVisibility': 'private'
        }), 200
    
# 更新隐私设置
@privacy_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_privacy_settings():
    logger.info('接收到更新设置请求')
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    logger.info(f'用户{user_id}的隐私设置更新数据：{data}')
    logger.info(f'data类型：{type(data)}')
    logger.info(f'request.data：{request.data}')
    
    # 检查data是否为None
    if data is None:
        logger.error('请求数据为空！')
        return jsonify({'message': '请求数据为空'}), 400

    # 查找用户的隐私设置
    settings = PrivacySettings.query.filter_by(user_id=user_id).first()
    
    if not settings:
        # 如果没有设置，创建新的设置
        settings = PrivacySettings(user_id=user_id)
        logger.info(f'用户{user_id}没有隐私设置，创建新记录')
    else:
        logger.info(f'找到用户{user_id}的隐私设置，当前值：{settings.personal_info_visibility}')

    # 更新设置
    if 'personalInfoVisibility' in data:
        visibility = data['personalInfoVisibility']
        logger.info(f'准备更新可见性为：{visibility}')
        # 验证可见性值
        if visibility in ['private', 'friends', 'public']:
            settings.personal_info_visibility = visibility
            logger.info(f'更新后的值：{settings.personal_info_visibility}')
        else:
            logger.error(f'无效的个人信息可见性值：{visibility}')
            return jsonify({'message': '无效的个人信息可见性设置'}), 400  
    else:
        logger.warning('请求中没有personalInfoVisibility字段')

    # 保存到数据库
    db.session.add(settings)
    db.session.commit()
    
    # 重新查询确认保存成功
    saved_settings = PrivacySettings.query.filter_by(user_id=user_id).first()
    logger.info(f'保存后从数据库查询的值：{saved_settings.personal_info_visibility if saved_settings else None}')

    logger.info(f'用户{user_id}的隐私设置更新成功')
    return jsonify(settings.to_dict()), 200