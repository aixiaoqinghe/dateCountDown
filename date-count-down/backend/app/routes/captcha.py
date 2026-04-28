# app/routes/captcha.py
from flask import Blueprint, session, make_response
from captcha.image import ImageCaptcha
import random
import string 

# 创建蓝图
captcha_bp = Blueprint('captcha', __name__)