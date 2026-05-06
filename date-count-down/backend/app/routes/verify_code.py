from flask import Blueprint, request, jsonify, session
from flask_mail import Message
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mail 
from app.models import User 
import random 
import string 
import logging 
import datetime 

logger = logging.getLogger(__name__)

# 从公共工具模块导入
from app.utils import (
    clean_phone_number,
    validate_phone_number,
    can_send_verify_code,
    record_send_time,
    is_code_expired
)

verify_code_bp = Blueprint('verify_code', __name__)
# 生成6位数字验证码
def generate_verify_code():
    return ''.join(random.choices(string.digits, k = 6))

# 发送邮箱验证码
@verify_code_bp.route('/send_email_code', methods=['POST'])
def send_email_code():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'message': '请输入邮箱'}), 400
    
    # 检查发送频率
    can_send, message = can_send_verify_code('email')
    if not can_send:
        logger.info(message)
        return jsonify({'message': message}), 429    # too many requests
    
    user = User.query.filter_by(email=email).first()
    if not user:
        logger.error(f'邮箱 {email} 未注册')
        return jsonify({'message': '该邮箱未注册'}), 400
    
    # 生成验证码
    code = generate_verify_code()

    # 保存验证码到session(有效期为5分钟)
    session['email_verify_code'] = code 
    session['email_verify_email'] = email
    session['email_verify_send_time'] = datetime.datetime.now().timestamp()
    session.permanent = True    # 设置session永久有效

    # 发送邮件
    msg = Message('倒计时APP验证码', recipients=[email])
    msg.body = f'您的验证码是:{code},有效期为5分钟。'

    try:
        mail.send(msg)
        record_send_time('email')    # 记录发送时间
        logger.info(f'验证码已发送到邮箱：{email}')
        return jsonify({'message': '验证码已发送'}), 200
    except Exception as e:
        logger.error(f'发送邮箱失败：{e}')
        return jsonify({'message': '发送失败，请稍后重试'}), 500
    
# 验证邮箱验证码
@verify_code_bp.route('/verify_email_code', methods=['POST'])
def verify_email_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    stored_code = session.get('email_verify_code')
    stored_email = session.get('email_verify_email')

    # 检查验证码是否过期
    if is_code_expired('email_verify'):
        session.pop('email_verify_code', None)
        session.pop('email_verify_email', None)
        session.pop('email_verify_send_time', None)
        return jsonify({'message': '验证码已过期，请重新获取'}), 400

    if not stored_code or not stored_email:
        logger.error(f'邮箱{email}验证码已过期，请重新获取')
        return jsonify({'message': '验证码已过期，请重新获取'}), 400  # 注意逗号
    
    if stored_email != email or stored_code != code:
        logger.error(f'邮箱{email}验证码错误')
        return jsonify({'message': '验证码错误'}), 400  
        session.pop('email_verify_send_time', None)
    
    # 验证成功，清除session
    session.pop('email_verify_code', None)  
    session.pop('email_verify_email', None) 
    session.pop('email_verify_send_time', None)
    
    # 验证成功，返回响应
    return jsonify({'message': '验证成功'}), 200

# 重置密码
@verify_code_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    phone = data.get('phone')
    code = data.get('code')
    new_password = data.get('new_password')

    # 判断是邮箱验证还是手机验证
    is_email_verify = bool(email)
    is_phone_verify = bool(phone)

    # 参数验证： 必须选择一种验证方式
    if not (is_email_verify ^ is_phone_verify):   # XOR 异或，只能选一个
        return jsonify({'message': '请选择邮箱或手机号验证'}), 400
    
    if is_email_verify:
        # 邮箱验证逻辑
        stored_code = session.get('email_verify_code')
        stored_target = session.get('email_verify_email')
        target = email
    else:
        # 手机验证逻辑(先清理格式)
        cleaned_phone = phone.strip().replace(' ', '').replace('-', '')
        if cleaned_phone.startswith('+86'):
            cleaned_phone = cleaned_phone[3:]

        # 获取手机验证的session
        stored_code = session.get('sms_verify_code')
        stored_target = session.get('sms_verify_phone')
        target = cleaned_phone
        

    if not stored_code or not stored_target:
        logger.error(f'{target}验证码已过期，请重新获取')
        return jsonify({'message': '验证码已过期，请重新获取'}), 400
    
    if stored_target != target or stored_code != code:
        logger.error(f'邮箱{target}验证码错误')
        return jsonify({'message': '验证码错误'}), 400
    
    # 根据验证方式查询用户
    if is_email_verify:
        user = User.query.filter_by(email=email).first()
    else:
        user = User.query.filter_by(phone=target).first()

    if not user:
        logger.error(f'用户 {target} 不存在')
        return jsonify({'message': '用户不存在'}), 400
    
    # 更新密码
    user.set_password(new_password)

    from app import db 
    db.session.commit()

    # 清除对应类型的session
    if is_email_verify:
        session.pop('email_verify_code', None)
        session.pop('email_verify_email', None)
    else:
        session.pop('sms_verify_code', None)
        session.pop('sms_verify_phone', None)
    

    logger.info(f'用户{target}密码重置成功')
    return jsonify({'message': '密码重置成功'}), 200

# 发送短信验证码
@verify_code_bp.route('/send_sms_code', methods=['POST'])
@jwt_required(optional=True)
def send_sms_code():
    data = request.get_json()
    phone = data.get('phone')

    # 参数验证
    if not phone:
        return jsonify({'message': '请输入手机号'}), 400
    
    # 使用封装的函数验证手机号
    cleaned_phone = validate_phone_number(phone) 
    if not cleaned_phone:
        logger.error(f'手机号{phone}格式错误')
        return jsonify({'message': '请输入正确的手机号'}), 400
    
    # 检查发送频率
    can_send, message = can_send_verify_code('sms_verify')
    if not can_send:
        return jsonify({'message': message}), 429

    # 获取当前登录用户（如果已登录）
    current_user_id = get_jwt_identity()
    
    if current_user_id:
        # 如果已登录，检查手机号是否属于当前用户
        user = User.query.get(current_user_id)
        if user and user.phone == cleaned_phone:
            # 生成验证码
            code = generate_verify_code()

            # 保存验证码到session
            session['sms_verify_code'] = code
            session['sms_verify_phone'] = cleaned_phone
            session['sms_verify_send_time'] = datetime.datetime.now().timestamp()
            session.permanent = True

            # 模拟发送短信
            logger.info(f'【模拟发送】向手机号 {cleaned_phone} 发送验证码： {code}')

            record_send_time('sms_verify')
            logger.info(f'手机号{cleaned_phone}验证码已发送')
            return jsonify({'message': '验证码已发送'}), 200
        else:
            logger.error(f'手机号 {cleaned_phone} 不属于当前用户')
            return jsonify({'message': '该手机号不属于当前用户'}), 400
    else:
        # 如果未登录，检查手机号是否已注册（用于忘记密码场景）
        user = User.query.filter_by(phone=cleaned_phone).first()
        if not user:
            logger.error(f'手机号 {cleaned_phone} 未注册')
            return jsonify({'message': '该手机号未注册'}), 400
        
        # 生成验证码
        code = generate_verify_code()

        # 保存验证码到session
        session['sms_verify_code'] = code
        session['sms_verify_phone'] = cleaned_phone
        session['sms_verify_send_time'] = datetime.datetime.now().timestamp()
        session.permanent = True

        # 模拟发送短信
        logger.info(f'【模拟发送】向手机号 {cleaned_phone} 发送验证码： {code}')

        record_send_time('sms_verify')
        logger.info(f'手机号{cleaned_phone}验证码已发送')
        return jsonify({'message': '验证码已发送'}), 200

# 验证短信验证码
@verify_code_bp.route('/verify_sms_code', methods=['POST'])
def verify_sms_code():
    data = request.get_json()
    phone = data.get('phone')
    code = data.get('code')

    # 使用封装的函数清理手机号
    cleaned_phone = clean_phone_number(phone)
    if not cleaned_phone:
        logger.error(f'手机号{phone}格式错误')
        return jsonify({'message': '请输入正确的手机号'}), 400
    
    stored_code = session.get('sms_verify_code')
    stored_phone = session.get('sms_verify_phone')

    # 检查验证码是否过期
    if is_code_expired('sms_verify'):
        session.pop('sms_verify_code', None)
        session.pop('sms_verify_phone', None)
        session.pop('sms_verify_send_time', None)
        return jsonify({'message': '验证码已过期，请重新获取'}), 400
    
    if not stored_code or not stored_phone:
        logger.error(f'手机号{cleaned_phone}验证码已过期，请重新获取')
        return jsonify({'message': '验证码已过期，请重新获取'}), 400
    
    if stored_phone != cleaned_phone or stored_code != code:
        logger.error(f'手机号{cleaned_phone}验证码错误')
        return jsonify({'message': '验证码错误'}), 400

    # 验证成功，清除session
    session.pop('sms_verify_code', None)
    session.pop('sms_verify_phone', None)
    session.pop('sms_verify_send_time', None)

    logger.info(f'手机号{stored_phone}验证成功')
    return jsonify({'message': '验证成功'}), 200