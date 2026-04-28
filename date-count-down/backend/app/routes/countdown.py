from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.countdown import Countdown 
from app import db
import logging
from datetime import datetime 
from app.utils.schemas import countdown_schema
from marshmallow import ValidationError
from app.utils.error_handlers import handle_errors, APIError

logger = logging.getLogger(__name__)

# 创建蓝图
countdown_bp = Blueprint('countdown', __name__)

# 创建倒计时
@countdown_bp.route('', methods=['POST'])
@jwt_required()
@handle_errors
def create_countdown():
    logger.info("=======创建倒计时请求开始=======")
    logger.info(f'请求方法：{request.method}')
    logger.info(f'请求路径：{request.path}')
    logger.info(f'请求头:{dict(request.headers)}')
    logger.info(f'请求体：{request.get_json()}')

    user_id = int(get_jwt_identity())
    data = request.get_json()
    logger.info(f'当前用户ID:{user_id}')
    logger.info(f'创建倒计时数据：{ data }')

    # 验证数据
    try:
        validated_data = countdown_schema.load(data)
    except ValidationError as err:
        logger.error(f'数据验证失败：{ err.messages}')
        return jsonify({'message': '数据验证失败', 'errors': err.messages}), 400
    
    # 验证日期格式
    try:
        countdown_schema.validate_target_date(data.get('target_date'))
    except ValidationError as err:
        logger.warning(f'日期格式验证失败：{ err.messages }')
        return jsonify({'message': err.messages[0]}), 400

    logger.info(f'创建倒计时数据： {validated_data}')    

    # 在验证失败时抛出自定义错误

    if not validated_data.get('task_name'):
        raise APIError('任务名称不能为空', 400)
    
    # 创建倒计时
    countdown = Countdown(
        user_id = user_id,
        task_name = validated_data['task_name'],
        target_date = datetime.fromisoformat(validated_data['target_date']),
        category = validated_data['category'],
        background_image = validated_data.get('background_image')
    )

    db.session.add(countdown)
    db.session.commit()
    logger.info(f'倒计时创建成功，ID: {countdown.id}')
    logger.info('=======创建倒计时请求结束=======')

    return jsonify({
        'id': countdown.id,
        'task_name': countdown.task_name,
        'target_date': countdown.target_date.isoformat(),
        'category': countdown.category,
        'background_image': countdown.background_image,
        'created_at': countdown.created_at.isoformat()
    }), 201

# 获取倒计时列表
@countdown_bp.route('', methods=['GET'])
@jwt_required()
def get_countdowns():
    logger.info('接受到获取倒计时列表请求')
    user_id = int(get_jwt_identity())
    countdowns = Countdown.query.filter_by(user_id = user_id).all()

    logger.info(f'获取到 {len(countdowns)} 个倒计时')
    return jsonify([{
        'id': countdown.id,
        'task_name': countdown.task_name,
        'target_date': countdown.target_date.isoformat(),
        'category': countdown.category,
        'background_image': countdown.background_image,
        'created_at': countdown.created_at.isoformat(),
        'updated_at': countdown.updated_at.isoformat()
    } for countdown in countdowns]), 200

# 获取倒计时详情
@countdown_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_countdown(id):
    logger.info(f'接收到获取倒计时详情请求，ID: {id}')
    user_id = int(get_jwt_identity())
    countdown = Countdown.query.filter_by(id = id, user_id = user_id).first()

    if not countdown:
        logger.warning(f'倒计时 ID {id} 不存在或无权限访问')
        return jsonify({'message': '倒计时不存在或无权限访问'}), 404
    
    logger.info(f'获取倒计时详情成功，ID: {id}')
    return jsonify({
        'id': countdown.id,
        'task_name': countdown.task_name,
        'target_date': countdown.target_date.isoformat(),
        'category': countdown.category,
        'background_image': countdown.background_image,
        'created_at': countdown.created_at.isoformat(),
        'updated_at': countdown.updated_at.isoformat()
    }), 200

# 更新倒计时
@countdown_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_countdown(id):
    logger.info(f'接收到更新倒计时请求，ID: {id}')
    user_id = int(get_jwt_identity())
    countdown = Countdown.query.filter_by(id = id, user_id = user_id).first()
    if not countdown:
        logger.warning(f'倒计时 ID {id} 不存在或无权限访问')
        return jsonify({'message': '倒计时不存在或无权限访问'}), 404
    
    data = request.get_json()
    logger.info(f'更新倒计时数据：{data}')

    # 更新字段
    if 'task_name' in data:
        countdown.task_name = data['task_name']
    if 'target_date' in data:
        countdown.target_date = datetime.fromisoformat(data['target_date'])
    if 'category' in data:
        countdown.category = data['category']
    if 'background_image' in data:
        countdown.background_image = data['background_image']

    db.session.commit()
    logger.info(f'倒计时更新成功，ID: {id}')

    return jsonify({
        'id': countdown.id,
        'task_name': countdown.task_name,
        'target_date': countdown.target_date.isoformat(),
        'category': countdown.category,
        'background_image': countdown.background_image,
        'updated_at': countdown.updated_at.isoformat()
    }), 200

# 删除倒计时
@countdown_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_countdown(id):
    logger.info(f'接收到删除倒计时请求，ID: {id}')
    user_id = int(get_jwt_identity())
    countdown = Countdown.query.filter_by(id = id, user_id = user_id).first()

    if not countdown:
        logger.warning(f'倒计时 ID {id} 不存在或无权限访问')
        return jsonify({'message': '倒计时不存在或无权限访问'}), 404
    
    db.session.delete(countdown)
    db.session.commit()
    logger.info(f'倒计时删除成功，ID: {id}')

    return jsonify({'message': '倒计时删除成功'}), 200