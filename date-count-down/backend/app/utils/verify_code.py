# backend/app/utils/verify_code/py

import re 
import random
import string 
import datetime
from flask import session 

# ======= 手机号处理 =======
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
def can_send_verify_code(session_key, cool_down_seconds=60):
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

# 工具函数：生成验证码
def generate_verify_code(length=6):
    """ 生成指定长度的验证码 """
    return ''.join(random.choices(string.digits, k=length))

# 工具函数：验证邮箱验证码格式
def validate_email(email):
    """ 验证邮箱格式，返回True或False """
    if not email:
        return False
    # 使用正则表达式验证邮箱格式
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))
