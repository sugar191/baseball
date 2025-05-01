from .base import *

log_dir = BASE_DIR / 'logs'
log_dir.mkdir(exist_ok=True)  # dev.py / staging.py の先頭に追加

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 読み込み失敗時に警告
assert SECRET_KEY != 'dummy_dev_key', "SECRET_KEY not properly set"

# ログ設定
LOGGING['handlers']['console'] = {
    'class': 'logging.StreamHandler',
    'formatter': 'verbose',
}

LOGGING['handlers']['file'] = {
    'level': 'DEBUG',
    'class': 'logging.FileHandler',
    'filename': log_dir / 'dev.log',
    'formatter': 'verbose',
}

LOGGING['loggers'] = {
    'django': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
        'propagate': True,
    },
    'players': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
        'propagate': False,
    },
}