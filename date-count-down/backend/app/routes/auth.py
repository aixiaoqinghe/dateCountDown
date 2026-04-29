from flask import Blueprint, request, jsonify 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db
import logging
from app.routes.captcha import verify_captcha

logger = logging.getLogger(__name__)

# 创建蓝图（用于分组路由）
auth_bp = Blueprint('auth', __name__)

# 注册接口
@auth_bp.route('/register', methods=['POST'])    # 定义了 POST/api/auth/register 接口
def register():
    logger.info('接收到注册请求')
    # 获取前端发送的JSON数据
    data = request.get_json()     # 获取前端发送的JSON数据
    logger.info(f'注册数据: {data}')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    input_captcha = data.get('captcha')

    # 验证验证码（先验证，再检查其他）
    if not input_captcha:
        logger.warning('请输入验证码')
        return jsonify({'message': '请输入验证码'}), 400
    
    if not verify_captcha(input_captcha):
        logger.warning(f'验证码错误：{input_captcha}')
        return jsonify({'message': '验证码错误'}), 400

    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        logger.warning(f'用户名 {username} 已存在')
        return jsonify({'message':'用户已存在'}), 400
    # 检查邮箱是否已存在
    if User.query.filter_by(email=email).first():
        logger.warning(f'邮箱 {email} 已存在')
        return jsonify({'message':'邮箱已存在'}), 400
    
    # 创建新用户
    user = User(username = username, email = email)     # 实例化User类
    user.set_password(password)   # 哈希处理密码
    db.session.add(user)   # 添加到数据库会话（临时存储，未写入数据库）
    db.session.commit()     # 提交会话，保存到MySQL
    logger.info(f'用户 {username} 注册成功')

    return jsonify({'message':'注册成功'}), 201 


# 登录接口
@auth_bp.route('/login', methods=['POST'])
def login():
    logger.info('接收到登录请求')
    # 获取前端发送的JSON数据
    data = request.get_json()
    logger.info(f'登录数据: {data}')
    username = data.get('username')
    password = data.get('password')

    # 查询用户
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        logger.warning(f'用户 {username} 登录失败：用户名或密码错误')
        return jsonify({'message':'用户名或密码错误'}), 401
    
    # 创建JWT令牌（用于后续身份认证）
    access_token = create_access_token(identity=str(user.id))
    logger.info(f'用户 {username} 登录成功')
    return jsonify({
        'access_token':access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200

# 获取用户信息接口（需要登录）
@auth_bp.route('/user', methods=['GET'])
@jwt_required()     # 要求携带JWT令牌
def get_user_info():
    logger.info('接收到获取用户信息请求')
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        logger.warning(f'用户ID {user_id} 不存在')
        return jsonify({'message': '用户不存在'}), 404
    
    logger.info(f'获取用户 {user.username} 信息成功')
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }), 200

# 更新用户资料接口（需要登录）
@auth_bp.route('/user', methods=['PUT'])
@jwt_required()
def update_user_info():
    logger.info('接收到更新用户资料请求')
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        logger.warning(f'用户ID {user_id} 不存在')
        return jsonify({'message': '用户不存在'}), 404
    
    data = request.get_json()
    logger.info(f'更新用户资料： {data}')

    # 更新用户名
    if 'username' in data:
        # 检查用户名是否已存在
        if User.query.filter_by(username=data['username']).first() and data['username'] and data['username'] != user.username:
            logger.warning(f'用户名 {data["username"]} 已存在')
            return jsonify({'message': '用户名已存在'}), 400
        user.username = data['username']

    # 更新邮箱
    if 'email' in data:
        # 检查邮箱是否已存在
        if User.query.filter_by(email=data['email']).first() and data['email'] != user.email:
            logger.warning(f'邮箱 {data["email"]} 已存在')
            return jsonify({'message':'邮箱已存在'}), 400
        user.email = data['email']

    # 更新昵称
    if 'nickname' in data:
        user.nickname = data['nickname']

    # 更新手机号
    if 'phone' in data:
        user.phone = data['phone']

    # 更新头像
    if 'avatar' in data:
        user.avatar = data['avatar']

    db.session.commit()   # 提交会话，保存到MySQL
    logger.info(f'用户 {user.username} 资料更新成功')
    return jsonify({'message': '资料更新成功'}), 200

# 修改密码接口（需要登录）
@auth_bp.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    logger.info('接收到修改密码请求')
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        logger.warning(f'用户ID {user_id} 不存在')
        return jsonify({'message': '用户不存在'}), 404
    
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    # 验证旧密码
    if not user.check_password(old_password):
        logger.warning(f'用户{ user.username }修改密码失败：旧密码错误')
        return jsonify({'message': '旧密码错误'}), 400
    
    # 设置新密码
    user.set_password(new_password)
    db.session.commit()

    logger.info(f'用户 { user.username } 修改密码成功')
    return jsonify({'message': '密码修改成功'}), 200

