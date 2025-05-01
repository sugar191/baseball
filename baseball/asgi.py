# ASGI設定ファイル
#
# このモジュールは、ASGIサーバーによって読み込まれるエントリポイントです。
# 詳細は公式ドキュメントを参照:
# https://docs.djangoproject.com/ja/5.1/howto/deployment/asgi/

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baseball.settings')

application = get_asgi_application()
