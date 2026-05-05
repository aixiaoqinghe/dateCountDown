from flask import Blueprint, request, jsonify, session
from flask_mail import Message
from app import mail 
from app.models import User 
import random 
import string 
import logging 

logger = logging.getLogger(__name__)

verify_code_bp = Blueprint('verify_code', __name__)

# 工具函数：清理手机号格式
def clean_phone_number(phone):
    """ 清理手机号格式，支持+86、空格、短横线等格式 """
    if not phone:
        return None
    
    # 去除空格和短横线
    cleaned = phone.strip().replace(' ', '').replace('-', '')

    # 去除 +86 前缀
    if cleaned.startswith('+86'):
        cleaned = cleaned[3:]
    elif cleaned.startswith('86'):
        cleaned = cleaned[2:]

    return cleaned

# 工具函数：验证手机号格式
def validate_phone_number(phone):
    """ 验证手机号格式是否正确，返回标准化的手机号 """
    cleaned = clean_phone_number(phone)
    if cleaned and cleaned.isdigit() and len(cleaned) == 11:
        return cleaned 
    return None 

# 工具函数：检查是否可以发送验证码
def can_send_verify_code(phone):
    """ 检查是否可以发送验证码（冷却时间）"""
    last_send_time = session.get(f'{session_key}_last_send_time')
    if last_send_time:
        current_time  = datetime.datetime.now().timestamp()
        if current_time - last_send_time < cool_down_seconds:
            remaining = int(cool_down_seconds - (current_time - last_send_time))
            return False, f'请{remaining}秒后再发送'
    return True, ''

# 工具函数：记录发送时间
def record_send_time(session_key):
    """ 记录发送验证码的时间 """
    session[f'{session_key}_last_send_time'] = datetime.datetime.now().timestamp()

# 工具函数：检查验证码是否过期
def is_code_expired(session_key, valid_minutes=5):
    """ 检查验证码是否过期 """
    send_time = session.get(f'{session_key}_send_time')
    if send_time:
        current_time = datetime.datetime.now().timestamp()
        if current_time - send_time > valid_minutes * 60:
            return True
    return False
    

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
    
    user = User.query.filter_by(email=email).first()
    if not user:
        logger.error(f'邮箱 {email} 未注册')
        return jsonify({'message': '该邮箱未注册'}), 400
    
    # 生成验证码
    code = generate_verify_code()

    # 保存验证码到session(有效期为5分钟)
    session['email_verify_code'] = code 
    session['email_verify_email'] = email
    session.permanent = True    # 设置session永久有效

    # 发送邮件
    msg = Message('倒计时APP验证码', recipients=[email])
    msg.body = f'您的验证码是:{code},有效期为5分钟。'

    try:
        mail.send(msg)
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

    if not stored_code or not stored_email:
        return jsonify({'message': '验证码已过期，请重新获取'}), 400  # 注意逗号
    
    if stored_email != email or stored_code != code:
        logger.error(f'邮箱{email}验证码错误')
        return jsonify({'message': '验证码错误'}), 400  # 注意逗号
    
    # 验证成功，清除session
    session.pop('email_verify_code', None)  # 注意逗号
    session.pop('email_verify_email', None)  # 注意逗号
    
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
def send_sms_code():
    data = request.get_json()
    phone = data.get('phone')

    # 参数验证
    if not phone:
        return jsonify({'message': '请输入手机号'}), 400
    
    # 清理手机号格式（支持 +86、空格、短横线等格式）
    cleaned_phone = phone.strip().replace(' ', '').replace('-', '')
    if cleaned_phone.startswith('+86'):
        cleaned_phone = cleaned_phone[3:]

    # 验证手机号格式
    if not cleaned_phone.isdigit() or len(cleaned_phone) != 11:
        return jsonify({'message': '请输入正确的手机号'}), 400
    
    # 查询用户
    user = User.query.filter_by(phone=cleaned_phone).first()
    if not user:
        logger.error(f'手机号 {cleaned_phone} 未注册')
        return jsonify({'message': '该手机号未注册'}), 400
    
    # 生成验证码
    code = generate_verify_code()

    # 保存验证码到session
    session['sms_verify_code'] = code
    session['sms_verify_phone'] = cleaned_phone
    session.permanent = True  # 设置session永久有效

    # 模拟发送短信（实际项目中需要；接入短信API）
    logger.info(f'【模拟发送】向手机号 {cleaned_phone} 发送验证码： {code}')

    return jsonify({'message': '验证码已发送'}), 200

# 验证短信验证码
@verify_code_bp.route('/verify_sms_code', methods=['POST'])
def verify_sms_code():
    data = request.get_json()
    phone = data.get('phone')
    code = data.get('code')

    # 清理手机号格式
    cleaned_phone = phone.strip().replace(' ', '').replace('-', '')
    if cleaned_phone.startswith('+86'):
        cleaned_phone = cleaned_phone[3:]

    stored_code = session.get('sms_verify_code')
    stored_phone = session.get('sms_verify_phone')

    if not stored_code or not stored_phone:
        return jsonify({'message': '验证码已过期，请重新获取'}), 400
    
    if stored_phone != cleaned_phone or stored_code != code:
        logger.error(f'手机号{cleaned_phone}验证码错误')
        return jsonify({'message': '验证码错误'}), 400
    
    # 验证成功，清除session
    session.pop('sms_verify_code', None)
    session.pop('sms_verify_phone', None)

    logger.info(f'手机号{stored_phone}验证成功')
    return jsonify({'message': '验证成功'}), 200



