from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.device import Device
import logging

# 创建蓝图
device_bp = Blueprint('device', __name__)
logger = logging.getLogger(__name__)

# 1.获取用户的设备列表
@device_bp.route('', methods=['GET'])
@jwt_required()
def get_devices():
    """ 获取用户的所有登录设备 """
    logger.info('接收到获取设备列表请求')
    user_id = int(get_jwt_identity())

    # 查询用户的所有设备，按最后登录时间排序
    devices = Device.query.filter_by(user_id=user_id).order_by(Device.last_login.desc()).all()

    # 获取当前请求的IP
    current_ip = request.remote_addr

    # 转换为前端需要的格式，并标记当前设备
    result = []
    for device in devices:
        device_dict = device.to_dict()
        # 根据IP判断是否当前设备
        device_dict['isCurrent'] = (device.ip == current_ip)
        result.append(device_dict)

    logger.info(f'用户{user_id}获取设备列表成功，共{len(result)} 台设备')
    return jsonify(result), 200

# 2.获取单个设备详情
@device_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_device(id):
    """ 获取单个设备详情 """
    logger.info(f'接收到获取设备详情请求,ID: {id}')
    user_id = int(get_jwt_identity())

    # 查询设备
    device = Device.query.filter_by(id=id, user_id=user_id).first()

    if not device:
        logger.warning(f'用户{user_id}访问不存在的设备, ID:{id}')
        return jsonify({'message':'设备不存在'}), 404
    
    # 转换为前端格式并标记是否当前设备
    device_dict = device.to_dict()
    device_dict['isCurrent'] = (device.ip == request.remote_addr)

    return jsonify(device_dict), 200

# 3.删除设备（退出登录该设备）
@device_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_device(id):
    """ 删除设备（退出登录）"""
    logger.info(f'接收到删除设备请求, ID:{id}')
    user_id = int(get_jwt_identity())

    # 查询设备
    device = Device.query.filter_by(id=id, user_id=user_id).first()

    # 获取请求体（使用silent=True避免解析错误）
    data = request.get_json(silent=True)
    current_device_id = None

    # 安全地获取current_device_id 
    if data and isinstance(data, dict):
        current_device_id = data.get('current_device_id')

    # 使用device_id判断是否当前设备（比IP更可靠）
    if current_device_id and device.device_id == current_device_id:
        logger.warning(f'用户{user_id}尝试删除当前设备')
        return jsonify({'message': '不能移除当前设备'}), 400
    
    # 删除设备
    db.session.delete(device)
    db.session.commit()

    logger.info(f'用户{user_id}删除设备成功, ID:{id}')
    return jsonify({'message': '设备已成功移除'}), 200

# 4.更新/创建设备信息（用户登录时调用）
@device_bp.route('/current', methods=['POST'])
@jwt_required()
def update_current_device():
    """ 更新或创建当前设备信息 """
    logger.info('接收到更新设备信息请求')
    user_id = int(get_jwt_identity())

    # 获取前端传递的数据
    data = request.get_json()

    # 获取客户端IP
    client_ip = request.remote_addr

    # 检查设备是否已存在（通过device_id判断）
    device = Device.query.filter_by(device_id=data.get('device_id')).first()

    if device:
        # 更新设备信息
        device.name = data.get('name')
        device.device_type = data.get('device_type')
        device.os = data.get('os')
        device.browser = data.get('browser')
        device.location = data.get('location')
        device.ip = client_ip
        device.last_login = datetime.now()
    else:
        # 创建新设备
        device = Device(
            user_id = user_id,
            device_id = data.get('device_id'),
            name = data.get('name'),
            device_type = data.get('device_type'),
            os = data.get('os'),
            browser = data.get('browser'),
            location = data.get('location'),
            ip = client_ip,
        )
        db.session.add(device)
    
    db.session.commit()

    # 返回设备信息，标记为当前设备
    device_dict = device.to_dict()
    device_dict['isCurrent'] = True

    logger.info(f'用户{user_id}更新设备信息成功')
    return jsonify(device_dict), 200