from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.version import AppVersion
from app import db
from app.decorators import admin_required
import logging
import json

logger = logging.getLogger(__name__)

# 创建蓝图
version_bp = Blueprint('version', __name__)

# 检查版本接口（公开接口，不需要登录）
@version_bp.route('/check', methods=['GET'])
def check_version():
    logger.info('接收到版本检查请求')

    # 获取当前版本参数
    current_version = request.args.get('version', '1.0.0')

    # 查找最新版本
    latest_version = AppVersion.query.filter_by(is_latest=True).first()

    if not latest_version:
        # 如果没有配置版本，返回默认信息
        logger.info('未找到最新版本配置， 返回默认版本信息')
        return jsonify({
            'currentVersion':current_version,
            'latestVersion': '1.0.0',
            'hasUpdate': False,
            'updateContent': [],
            'forceUpdate': False
        }), 200
    
    # 比较版本号
    has_update = compare_versions(current_version, latest_version.version_number) > 0
    force_update = latest_version.force_update

    # 解析更新内容
    update_content = []
    if latest_version.update_content:
        try:
            import json
            update_content = json.loads(latest_version.update_content)
        except:
            update_content = latest_version.update_content.split(';')

    version_info = {
        'currentVersion':current_version,
        'latestVersion': latest_version.version_number,
        'hasUpdate': has_update,
        'updateContent': update_content,
        'forceUpdate': force_update,
        'minSupportVersion': latest_version.min_support_version
    }        

    logger.info(f'版本检查结果：{version_info}')
    return jsonify(version_info), 200

# 添加新版本（需要管理员权限）
@version_bp.route('/add', methods=['POST'])
@admin_required
def add_version():
    logger.info('接收到添加版本请求')
    user_id = int(get_jwt_identity())

    data = request.get_json()

    # 验证必要字段
    if not data.get('versionNumber'):
        return jsonify({'message': '版本号不能为空'}), 400
    
    # 处理 update_content，如果是数组则转换为JSON字符串
    update_content = data.get('updateContent', '')
    if isinstance(update_content, list):
        update_content = json.dumps(update_content)
    
    # 创建新版本
    new_version = AppVersion(
        version_number=data['versionNumber'],
        update_content=update_content,
        download_url=data.get('downloadUrl', ''),
        min_support_version=data.get('minSupportVersion', '1.0.0'),
        force_update=data.get('forceUpdate', False),
        is_latest=data.get('isLatest', False)
    )

    # 如果设为最新版本，取消其他版本的最新标记
    if new_version.is_latest:
        AppVersion.query.update({AppVersion.is_latest: False})

    db.session.add(new_version)
    db.session.commit()

    logger.info(f'版本{new_version.version_number}添加成功')
    return jsonify(new_version.to_dict()), 201

# 更新版本信息（需要管理员权限）
@version_bp.route('/<int:version_id>', methods=['PUT'])
@admin_required
def update_version(version_id):
    logger.info(f'接收到更新版本请求，版本ID:{version_id}')

    version = AppVersion.query.get(version_id)
    if not version:
        return jsonify({'message': '版本不存在'}), 404
    
    data = request.get_json()

    if 'versionNumber' in data:
        version.version_number = data['versionNumber']
    if 'updateContent' in data:
        update_content = data['updateContent']
        # 如果是数组，转换为JSON字符串存储
        if isinstance(update_content, list):
            update_content = json.dumps(update_content)
        version.update_content = update_content
    if 'downloadUrl' in data:
        version.download_url = data['downloadUrl']
    if 'minSupportVersion' in data:
        version.min_support_version = data['minSupportVersion']
    if 'forceUpdate' in data:
        version.force_update = data['forceUpdate']
    if 'isLatest' in data:
        # 如果设为最新版本，取消其他版本的最新标记
        AppVersion.query.update({AppVersion.is_latest: False})
        version.is_latest = True

    db.session.commit()

    logger.info(f'版本{version.version_number}更新成功')
    return jsonify(version.to_dict()), 200

# 删除版本（需要管理员权限）
@version_bp.route('/<int:version_id>', methods=['DELETE'])
@admin_required
def delete_version(version_id):
    logger.info(f'接收到删除版本请求，版本ID:{version_id}')
    
    version = AppVersion.query.get(version_id)
    if not version:
        logger.error(f'版本{version_id}不存在')
        return jsonify({'message': '版本不存在'}), 404
    
    db.session.delete(version)
    db.session.commit()
    
    logger.info(f'版本{version.version_number}删除成功')
    return jsonify({'message': '版本删除成功'}), 200
    
# 获取版本列表（需要管理员权限）
@version_bp.route('/list', methods=['GET'])
@admin_required
def get_version_list():
    logger.info('接收到获取版本列表请求')

    versions = AppVersion.query.order_by(AppVersion.created_at.desc()).all()
    version_list = [v.to_dict() for v in versions]

    return jsonify(version_list), 200

# 版本号比较函数
def compare_versions(v1, v2):
    """ 比较两个版本号，返回正数表示v2>v1,负数表示v1>v2,0表示相等 """
    parts1 = list(map(int, v1.split('.')))
    parts2 = list(map(int, v2.split('.')))

    # 补齐长度
    max_len = max(len(parts1), len(parts2))
    parts1 += [0] * (max_len - len(parts1))
    parts2 += [0] * (max_len - len(parts2))

    for i in range(max_len):
        if parts2[i] > parts1[i]:
            return 1
        elif parts2[i] < parts1[i]:
            return -1
    
    return 0