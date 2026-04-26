from flask import Blueprint, jsonify
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
version_bp = Blueprint('version', __name__)

# 检查版本接口
@version_bp.route('/check', methods=['GET'])
def check_version():
    logger.info('接收到版本检查请求')
    # 模拟版本信息（可以从数据库或配置文件读取）
    version_info = {
        'current_version': '1.0.0',
        'latest_version': '2.0.0',
        'has_update': True,
        'update_content': [
            '新增多种倒计时模板',
            '优化用户界面',
            '提升系统性能',
            '修复已知bug'
        ]
    }
    logger.info(f'版本信息: {version_info}')
    return jsonify(version_info), 200