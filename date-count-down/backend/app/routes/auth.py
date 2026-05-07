from flask import Blueprint, request, jsonify 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db
import logging
from app.routes.captcha import verify_captcha

logger = logging.getLogger(__name__)

# 从公共工具模块导入
from app.utils import (
    clean_phone_number,
    validate_phone_number,
    generate_verify_code,
    can_send_verify_code,
    record_send_time,
    is_code_expired,
    validate_email
)

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
            'email': user.email,
            'avatar': user.avatar,
            'nickname': user.nickname,
            'phone': user.phone
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
        'avatar': user.avatar,
        'nickname': user.nickname,
        'phone': user.phone,
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

# 发送修改邮箱验证码
@auth_bp.route('/send_change_email_code', methods=['POST'])
@jwt_required()
def send_change_email_code():
    from flask import session
    from flask_mail import Message
    from app import mail
    import random
    import string
    import datetime
    
    data = request.get_json()
    new_email = data.get('email')
    
    if not new_email:
        logger.error(f'邮箱{new_email}格式错误') 
        return jsonify({'message': '请输入新邮箱'}), 400
    
    # 验证邮箱格式
    if not validate_email(new_email):
        logger.error(f'邮箱{new_email}格式错误')
        return jsonify({'message': '请输入正确的邮箱'}), 400
    
    # 检查新邮箱是否已被使用
    existing_user = User.query.filter_by(email=new_email).first()
    if existing_user:
        return jsonify({'message': '该邮箱已被注册'}), 400
    
    # 检查发送频率
    can_send, message = can_send_verify_code('change_email')
    if not can_send:
        return jsonify({'message': message}), 429
    
    # 生成验证码
    code = generate_verify_code()
    
    # 保存验证码到session
    session['change_email_code'] = code
    session['change_email_email'] = new_email
    session['change_email_send_time'] = datetime.datetime.now().timestamp()
    session.permanent = True
    
    # 发送邮件
    msg = Message('倒计时APP邮箱验证', recipients=[new_email])
    msg.body = f'您的验证码是:{code},有效期为5分钟。'
    
    try:
        mail.send(msg)
        logger.info(f'修改邮箱验证码已发送到：{new_email}')
        return jsonify({'message': '验证码已发送'}), 200
    except Exception as e:
        logger.error(f'发送邮箱失败：{e}')
        return jsonify({'message': '发送失败，请稍后重试'}), 500

# 修改邮箱
@auth_bp.route('/change_email', methods=['POST'])
@jwt_required()
def change_email():
    from flask import session
    
    data = request.get_json()
    new_email = data.get('email')
    verification_code = data.get('verification_code')
    
    if not new_email:
        return jsonify({'message': '请输入新邮箱'}), 400
    
    if not verification_code:
        return jsonify({'message': '请输入验证码'}), 400
    
    # 获取当前用户
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 400
    
    # 验证验证码
    stored_code = session.get('change_email_code')
    stored_email = session.get('change_email_email')
    
    if not stored_code or not stored_email:
        return jsonify({'message': '验证码已过期，请重新获取'}), 400
    
    if stored_email != new_email or stored_code != verification_code:
        return jsonify({'message': '验证码错误'}), 400
    
    # 更新邮箱
    user.email = new_email
    db.session.commit()
    
    # 清除session
    session.pop('change_email_code', None)
    session.pop('change_email_email', None)
    session.pop('change_email_last_send_time', None)
    
    logger.info(f'用户 {user.username} 邮箱修改成功')
    return jsonify({'message': '邮箱修改成功', 'user': {'email': new_email}}), 200

# 发送绑定手机号验证码
@auth_bp.route('/send_bind_phone_code', methods=['POST'])
@jwt_required()
def send_bind_phone_code():
    from flask import session
    import random
    import string
    import datetime
    
    data = request.get_json()
    phone = data.get('phone')

    if not phone:
        return jsonify({'message': '请输入手机号'}), 400
    
    # 使用公共模块的验证函数
    cleaned_phone = validate_phone_number(phone)
    if not cleaned_phone:
        logger.error(f'手机号{phone}格式错误')
        return jsonify({'message': '请输入正确的手机号'}), 400
    
    # 检查手机号是否已被使用
    existing_user = User.query.filter_by(phone=cleaned_phone).first()
    if existing_user:
        logger.error(f'手机号{cleaned_phone}已被绑定')
        return jsonify({'message': '该手机号已被绑定'}), 400
    
    # 使用 can_send_verify_code 检查频率
    can_send, message = can_send_verify_code('bind_phone')
    if not can_send:
        return jsonify({'message': message}), 429
    
    # 生成验证码
    code = generate_verify_code()

    # 保存验证码到session
    session['bind_phone_code'] = code
    session['bind_phone_phone'] = cleaned_phone
    session['bind_phone_send_time'] = datetime.datetime.now().timestamp()
    session.permanent = True

    # 模拟发送短信
    logger.info(f'【模拟发送】向手机号{cleaned_phone}发送验证码：{code}')

    # 记录发送时间
    record_send_time('bind_phone')

    logger.info(f'用户绑定手机号验证码已发送到：{cleaned_phone}')
    return jsonify({'message': '验证码已发送'}), 200

# 绑定手机号
@auth_bp.route('/bind_phone', methods=['POST'])
@jwt_required()
def bind_phone():
    data = request.get_json()
    phone = data.get('phone')
    verification_code = data.get('verification_code')

    if not phone:
        logger.error('手机号不能为空')
        return jsonify({'message': '请输入手机号'}), 400
    
    if not verification_code:
        logger.error('验证码不能为空')
        return jsonify({'message': '请输入验证码'}), 400
    
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        logger.error(f'用户{current_user_id}不存在')
        return jsonify({'message': '用户不存在'}), 400
    
    cleaned_phone = validate_phone_number(phone)
    if not cleaned_phone:
        logger.error(f'手机号{phone}格式错误')
        return jsonify({'message': '请输入正确的手机号'}), 400
    
    # 检查验证码是否过期
    if is_code_expired('bind_phone'):
        session.pop('bind_phone_code', None)
        session.pop('bind_phone_phone', None)
        session.pop('bind_phone_send_time', None)
        logger.error(f'验证码已过期：{verification_code}')
        return jsonify({'message': '验证码已过期，请重新获取'}), 400

    # 获取session中的验证码
    stored_code = session.get('bind_phone_code')
    stored_phone = session.get('bind_phone_phone')
    
    if not stored_code or not stored_phone:
        logger.error(f'验证码已过期：{verification_code}')
        return jsonify({'message': '验证码已过期，请重新获取'}), 400
    
    if stored_code != cleaned_phone or stored_code != verification_code:
        logger.error(f'验证码错误：{verification_code}')
        return jsonify({'message': '验证码错误'}), 400
    
    user.phone = cleaned_phone
    db.session.commit()

    session.pop('bind_phone_code', None)
    session.pop('bind_phone_phone', None)
    session.pop('bind_phone_send_time', None)

    logger.info(f'用户{user.username}绑定手机号成功')
    return jsonify({'message': '手机号绑定成功', 'user': {'phone': cleaned_phone}}), 200

# 发送修改手机号验证码
@auth_bp.route('/send_change_phone_code', methods=['POST'])
@jwt_required()
def send_change_phone_code():
    from flask import session
    import random
    import string
    import datetime
    
    data = request.get_json()
    phone = data.get('phone')

    if not phone:
        logger.error('手机号不能为空')
        return jsonify({'message': '请输入手机号'}), 400
    
    cleaned_phone = validate_phone_number(phone)
    if not cleaned_phone:
        logger.error(f'手机号{phone}格式错误')
        return jsonify({'message': '请输入正确的手机号'}), 400
    
    # 检查手机号是否已被使用
    existing_user = User.query.filter_by(phone=cleaned_phone).first()
    if existing_user:
        logger.error(f'手机号{cleaned_phone}已被绑定')
        return jsonify({'message': '该手机号已被绑定'}), 400
    
    # 使用 can_send_verify_code 检查频率
    can_send, message = can_send_verify_code('change_phone')
    if not can_send:
        return jsonify({'message': message}), 429
    
    # 生成验证码
    code = generate_verify_code()

    # 保存验证码到session
    session['change_phone_code'] = code
    session['change_phone_phone'] = cleaned_phone
    session['change_phone_send_time'] = datetime.datetime.now().timestamp()
    session.permanent = True

    # 模拟发送短信
    logger.info(f'【模拟发送】向手机号{cleaned_phone}发送验证码：{code}')

    # 记录发送时间
    record_send_time('change_phone')
    
    logger.info(f'用户修改手机号验证码已发送到：{cleaned_phone}')
    return jsonify({'message': '验证码已发送'}), 200

# 修改手机号
@auth_bp.route('/change_phone', methods=['POST'])
@jwt_required()
def change_phone():
    data = request.get_json()
    phone = data.get('phone')
    verification_code = data.get('verification_code')

    if not phone:
        logger.error('手机号不能为空')
        return jsonify({'message': '请输入手机号'}), 400
    
    if not verification_code:
        logger.error('验证码不能为空')
        return jsonify({'message': '请输入验证码'}), 400
    
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        logger.error(f'用户{current_user_id}不存在')
        return jsonify({'message': '用户不存在'}), 400
    
    # 检查用户是否已绑定手机号
    if not user.phone:
        return jsonify({'message': '用户未绑定手机号'}), 400
    
    cleaned_phone = validate_phone_number(phone)
    if not cleaned_phone:
        logger.error(f'手机号{phone}格式错误')
        return jsonify({'message': '请输入正确的手机号'}), 400
    
    # 检查验证码是否过期
    if is_code_expired('change_phone'):
        session.pop('change_phone_code', None)
        session.pop('change_phone_phone', None)
        session.pop('change_phone_send_time', None)
        logger.error(f'验证码已过期：{verification_code}')
        return jsonify({'message': '验证码已过期，请重新获取'}), 400        
    
    # 获取session中的验证码
    stored_code = session.get('change_phone_code')
    stored_phone = session.get('change_phone_phone')

    if not stored_code or not stored_phone:
        logger.error(f'验证码已过期：{verification_code}')
        return jsonify({'message': '验证码已过期，请重新获取'}), 400
    
    if stored_code != cleaned_phone or stored_code != verification_code:
        logger.error(f'验证码错误：{verification_code}')
        return jsonify({'message': '验证码错误'}), 400
    
    # 更新用户手机号
    user.phone = cleaned_phone
    db.session.commit()

    # 清除session中的验证码
    session.pop('change_phone_code', None)
    session.pop('change_phone_phone', None)
    session.pop('change_phone_send_time', None)

    logger.info(f'用户{user.username}修改手机号成功')
    return jsonify({'message': '手机号修改成功', 'user': {'phone': cleaned_phone}}), 200