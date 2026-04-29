# app/routes/captcha.py
from flask import Blueprint, session, make_response
from captcha.image import ImageCaptcha
import random
import string 
from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
captcha_bp = Blueprint('captcha', __name__)

# 生成随机验证码文本
def generate_captcha_text(length = 6):
    """ 生成指定长度的随机验证码"""
    # 可选字符： 数字 + 大写字母（去掉容易混淆的字符：0/O, 1/I/l）
    chars = '23456789ABCDEFGHJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(chars) for _ in range(length))

# 获取验证码图片接口
@captcha_bp.route('/captcha')
def get_captcha():
    """ 生成并返回验证码图片 """
    # 1.生成验证码文本
    captcha_text = generate_captcha_text()

    # 2.存储到session(用于后续验证)
    session['captcha'] = captcha_text

    # 3.生成验证码图片
    image = ImageCaptcha(
        width = 120,    # 图片宽度
        height = 40,    # 图片高度
        font_sizes = [28]    # 字体大小（注意是复数形式）
    )

    # 生成图片数据
    image_data = image.generate(captcha_text)

    # 4.构建响应
    response = make_response(image_data.getvalue())
    response.headers['Content-Type'] = 'image/png'    # 设置响应类型为图片
    return response 

# 验证验证码函数
def verify_captcha(input_captcha):
    """ 验证用户输入的验证码是否正确 """
    # 1.从session获取存储的验证码
    stored_captcha = session.get('captcha')

    # 2.立即清除session中的验证码（防止重复使用）
    session.pop('captcha', None)

    # 3.验证（不区分大小写）
    if stored_captcha and input_captcha.lower() == stored_captcha.lower():
        return True
    return False

@captcha_bp.route('/verify-captcha', methods=['POST'])
def check_captcha():
    """ 验证验证码接口 """
    data = request.get_json()
    input_captcha = data.get('captcha')

    if verify_captcha(input_captcha):
        return jsonify({'success': True}), 200
    else:
        logger.error(f'验证码错误：{input_captcha}')
        return jsonify({'success': False, 'message': '验证码错误'}), 400