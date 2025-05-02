from .base import *

log_dir = BASE_DIR / 'logs'
log_dir.mkdir(exist_ok=True)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['160.251.200.53',]

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-random-secret-key')

# ログ設定
LOGGING['handlers']['file'] = {
    'level': 'INFO',
    'class': 'logging.FileHandler',
    'filename': log_dir / 'live.log',
    'formatter': 'verbose',
}

LOGGING['loggers'] = {
    'django': {
        'handlers': ['file'],
        'level': 'INFO',
        'propagate': True,
    },
    'players': {
        'handlers': ['file'],
        'level': 'INFO',
        'propagate': False,
    },
}