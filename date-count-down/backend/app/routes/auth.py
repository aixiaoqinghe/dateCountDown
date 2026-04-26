from flask import Blueprint, request, jsonify 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db

# 创建蓝图（用于分组路由）
auth_bp = Blueprint('auth', __name__)

# 注册接口
@auth_bp.route('/register', methods=['POST'])    # 定义了 POST/api/auth/register 接口
def register():
    # 获取前端发送的JSON数据
    data = request.get_json()     # 获取前端发送的JSON数据
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'message':'用户已存在'}), 400
    # 检查邮箱是否已存在
    if User.query.filter_by(email=email).first():
        return jsonify({'message':'邮箱已存在'}), 400
    
    # 创建新用户
    user = User(username = username, email = email)     # 实例化User类
    user.set_password(password)   # 哈希处理密码
    db.session.add(user)   # 添加到数据库会话（临时存储，未写入数据库）
    db.session.commit()     # 提交会话，保存到MySQL

    return jsonify({'message':'注册成功'}), 201

# 登录接口
@auth_bp.route('/login', methods=['POST'])
def login():
    # 获取前端发送的JSON数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 查询用户
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message':'用户名或密码错误'}), 401
    
    # 创建JWT令牌（用于后续身份认证）
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'access_token':access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200