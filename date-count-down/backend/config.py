import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'e7c3640ebf0f26a1fc46c1fa0b59be96')
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///countdown.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'e7c3640ebf0f26a1fc46c1fa0b59be96')
    JWT_ACCESS_TOKEN_EXPIRES = 7 * 24 * 60 * 60
    
    if DATABASE_URI.startswith('mysql'):
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': 20,
            'max_overflow': 50,
            'pool_timeout': 60,
            'pool_recycle': 300,
            'echo': False
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {}