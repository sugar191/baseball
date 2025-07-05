from .base import *

log_dir = BASE_DIR / "logs"
log_dir.mkdir(exist_ok=True)  # dev.py / staging.py の先頭に追加

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# 読み込み失敗時に警告
assert SECRET_KEY != "dummy_dev_key", "SECRET_KEY not properly set"

# ログ設定
LOGGING["handlers"]["console"] = {
    "class": "logging.StreamHandler",
    "formatter": "verbose",
}

LOGGING["handlers"]["file"] = {
    "level": "DEBUG",
    "class": "logging.handlers.TimedRotatingFileHandler",  # ← ここを変更
    "filename": log_dir / "dev.log",
    "formatter": "verbose",
    "when": "midnight",  # 毎日ローテーション
    "backupCount": 7,  # 過去7日分保持
    "encoding": "utf-8",  # 日本語ログ対策
}

LOGGING["loggers"] = {
    "django": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
        "propagate": True,
    },
    "players": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
        "propagate": False,
    },
}
