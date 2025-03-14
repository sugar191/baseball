# development.py
from .base import *  # base.pyの全設定をインポート

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'sugar191.pythonanywhere.com',
]


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sugar191$baseball',  # 作成したデータベース名
        'USER': 'baseball_user',  # MySQLのユーザー名
        'PASSWORD': 'password',  # MySQLのパスワード
        'HOST': 'localhost',  # MySQLがローカルにインストールされている場合
        'PORT': '3306',  # MySQLのポート番号（デフォルト）
    }
}