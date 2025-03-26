import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')  # .envを読み込む

application = get_wsgi_application()
