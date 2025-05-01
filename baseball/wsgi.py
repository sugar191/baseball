import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
from pathlib import Path

# プロジェクトのルートディレクトリにある .env ファイルを読み込む
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baseball.settings')  # 明示的に追加

application = get_wsgi_application()
