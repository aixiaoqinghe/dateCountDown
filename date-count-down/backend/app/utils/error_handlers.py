from flask import jsonify
from functools import wraps 
import logging 

logger = logging.getLogger(__name__)

def handle_errors(f):
    # 统一错误处理装饰器
    @wraps(f)       # 保留原函数的元信息
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f'服务器内部错误：{str(e)}')
            return jsonify({'message': '服务器内部错误', 'error': str(e)}), 500
    return decorated_function

# 自定义错误
class APIError(Exception):
    def __init__(self, message, status_code = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code