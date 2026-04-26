from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.feedback import Feedback
from app import db

# 创建蓝图
feedback_bp = Blueprint('feedback', __name__)

# 提交反馈接口（需要登录）
@feedback_bp.route('/submit', methods=['POST'])
@jwt_required()     # 要求携带JWT令牌
def submit_feedback():
    # 获取前端发送的JSON数据
    data = request.get_json()
    user_id = get_jwt_identity()   # 从JWT令牌中获取用户ID
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

    return jsonify({'message':'反馈提交成功'}), 201

