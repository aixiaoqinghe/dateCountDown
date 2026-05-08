from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.feedback import Feedback
from app import db
import logging
from flask_mail import Message
from app import mail

logger = logging.getLogger(__name__)

# 管理员邮箱配置
ADMIN_EMAIL = 'xiaoqinghe_verify@163.com'

# 反馈类型映射（英文转中文）
FEEDBACK_TYPE_MAP = {
    'suggestion': '功能建议',
    'bug': 'Bug反馈',
    'performance': '性能问题',
    'ui': '界面设计',
    'experience': '用户体验',
    'other': '其他'
}

# 创建蓝图
feedback_bp = Blueprint('feedback', __name__)

# 提交反馈接口（需要登录）
@feedback_bp.route('/submit', methods=['POST'])
@jwt_required()     # 要求携带JWT令牌
def submit_feedback():
    logger.info('接收到反馈提交请求')
    # 获取前端发送的JSON数据
    data = request.get_json()
    logger.info(f'反馈数据: {data}')
    user_id = int(get_jwt_identity())   # 从JWT令牌中获取用户ID，并转换为整数
    logger.info(f'用户ID: {user_id}')
    rating = data.get('rating')
    feedback_type = data.get('feedback_type')
    content = data.get('content')

    # 创建反馈记录
    feedback = Feedback(
        user_id = user_id,
        rating = rating,
        feedback_type = feedback_type,
        content = content
    )

    db.session.add(feedback)    # 添加到数据库会话
    db.session.commit()    # 提交会话，保存到MySQL
    logger.info(f'反馈提交成功，用户ID: {user_id}')

    # 发送邮件通知管理员
    try:
        # 将英文反馈类型转换为中文
        feedback_type_cn = FEEDBACK_TYPE_MAP.get(feedback_type, feedback_type)
        
        msg = Message(
            subject=f'【倒计时APP】新反馈通知',
            recipients=[ADMIN_EMAIL],
            body=f'''新收到一条用户反馈：

用户ID: {user_id}
评分: {'★' * rating} ({rating}星)
反馈类型: {feedback_type_cn}
反馈内容:
{content}

---
倒计时APP 自动发送'''
        )
        mail.send(msg)
        logger.info(f'反馈邮件已发送到管理员邮箱：{ADMIN_EMAIL}')
    except Exception as e:
        logger.error(f'发送反馈邮件失败：{e}')

    return jsonify({'message':'反馈提交成功'}), 201